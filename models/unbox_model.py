import sqlite3
import shutil
from pathlib import Path
import os

class Unbox_Model:
    """
    Classe para lógica de negócio e gerenciamento de estado.
    Atualizada com Locations, Staff e Controle de Estoque Mínimo.
    """
    
    def __init__(self):
        self.conn = None
        self.initialize_database() 
        self.conn.execute("PRAGMA foreign_keys = ON")
        cur = self.conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                building TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                role TEXT DEFAULT 'Professor'
            )
        """)
            
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT UNIQUE,
                category_id INTEGER,
                location_id INTEGER,
                quantity_available INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 1,
                FOREIGN KEY (category_id) REFERENCES categories(id),
                FOREIGN KEY (location_id) REFERENCES locations(id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_id INTEGER,
                staff_id INTEGER,
                type TEXT NOT NULL, 
                quantity INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventory_id) REFERENCES inventory(id),
                FOREIGN KEY (staff_id) REFERENCES staff(id)
            )
        """)
        
        self.conn.commit()


    def initialize_database(self):
        """
        Inicializa o banco de dados da aplicação.
        """
        base_path = Path.home()
        documents_path = base_path / "Documents"
        db_destination = documents_path / "inventory.db"
        db_template = Path("inventory_template.db")
        documents_path.mkdir(parents=True, exist_ok=True)

        if not db_destination.exists():
            print(f"[INFO] Banco não encontrado em: {db_destination}")
            try:
                if db_template.exists():
                    shutil.copy(db_template, db_destination)
                    print(f"[OK] Banco copiado do template com sucesso.")
                else:
                    print(f"[AVISO] Template '{db_template}' não encontrado. Criando banco vazio.")
            except Exception as e:
                print(f"[X] Erro de permissão/cópia: {e}")
        else:
            print(f"[INFO] Banco encontrado em: {db_destination}")
            
        self.conn = sqlite3.connect(str(db_destination))
        

    def create_location(self, name, building="Principal"):
        """Cria um novo local (location) no banco de dados."""
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT OR IGNORE INTO locations (name, building) VALUES (?, ?)", (name, building))
            self.conn.commit()
            print(f"[OK] Local '{name}' criado.")
        except Exception as e:
            print(f"[X] Erro ao criar local: {e}")
            

    def create_staff(self, name, role="Professor"):
        """Cria um novo membro da equipe no banco de dados."""
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT OR IGNORE INTO staff (name, role) VALUES (?, ?)", (name, role))
            self.conn.commit()
            print(f"[OK] Staff '{name}' criado.")
        except Exception as e:
            print(f"[X] Erro ao criar staff: {e}")


    def create_category(self, name):
        """Cria uma nova categoria no banco de dados."""
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Categoria: {e}")
            

    def create_item(self, name, serial_number, category_name, location_name, min_stock=1):
        """Cria um novo item no inventário."""
        try:
            cur = self.conn.cursor()
            
            cur.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            cat_res = cur.fetchone()
            cur.execute("SELECT id FROM locations WHERE name = ?", (location_name,))
            loc_res = cur.fetchone()

            if cat_res and loc_res:
                category_id = cat_res[0]
                location_id = loc_res[0]
                
                cur.execute("""
                    INSERT INTO inventory (name, serial_number, category_id, location_id, min_stock, quantity_available) 
                    VALUES (?, ?, ?, ?, ?, 0)""", 
                    (name, serial_number, category_id, location_id, min_stock)
                )
                self.conn.commit()
                print(f"[OK] Item '{name}' criado em '{location_name}'.")
                
            else:
                print(f"[X] Erro: Categoria '{category_name}' ou Local '{location_name}' não encontrados.")
                            
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Item: {e}")


    def register_movement(self, serial_number, movement_type, quantity, staff_name):
        """Registra um movimento de entrada ou saída de um item no inventário."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, quantity_available FROM inventory WHERE serial_number = ?", (serial_number,))
            if not (item := cursor.fetchone()):
                 raise ValueError("Item não encontrado.")
            inventory_id, current_stock = item

            cursor.execute("SELECT id FROM staff WHERE name = ?", (staff_name,))
            if not (staff_res := cursor.fetchone()):
                 raise ValueError(f"Funcionário '{staff_name}' não cadastrado.")
            staff_id = staff_res[0]
            
            delta = -quantity if movement_type == 'OUT' else quantity
            
            if movement_type == 'OUT' and current_stock < quantity:
                raise ValueError(f"Estoque insuficiente! Disponível: {current_stock}")

            new_stock = current_stock + delta

            cursor.execute("UPDATE inventory SET quantity_available = ? WHERE id = ?", (new_stock, inventory_id))
            cursor.execute("""
                INSERT INTO movements (inventory_id, staff_id, type, quantity) 
                VALUES (?, ?, ?, ?)""", (inventory_id, staff_id, movement_type, quantity)
            )

            self.conn.commit()
            print(f"[OK] Movimento '{movement_type}' registrado para {staff_name}.")

        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro Movimento: {e}")
            raise
            
            
    def get_dashboard_stats(self):
        """Recupera estatísticas do painel de controle do inventário."""
        try:
            cur = self.conn.cursor()
            stats = {}
            
            # IMPLEMENTAÇÃO: Alerta de estoque baixo (qtd <= min_stock)
            cur.execute("SELECT COUNT(*) FROM inventory WHERE quantity_available <= min_stock AND quantity_available > 0")
            stats['low_stock'] = cur.fetchone()[0]
            
            cur.execute("SELECT COALESCE(SUM(quantity), 0) FROM movements WHERE type = 'OUT'")
            stats['borrowed_items'] = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM inventory")
            stats['total_items'] = cur.fetchone()[0]

            return stats

        except Exception as e:
            print(f"[X] Erro: {e}")
            return {'low_stock': 0, 'borrowed_items': 0, 'total_items': 0}
            

    def get_items_paginated(self, page_number=1, page_size=20):
        """Recupera itens do inventário com paginação."""
        try:
            cur = self.conn.cursor()
            offset = (page_number - 1) * page_size
                
            cur.execute("""
                SELECT * FROM inventory 
                LIMIT ? OFFSET ?
            """, (page_size, offset))
                
            items = cur.fetchall()
            return items

        except Exception as e:
            print(f"[X] Erro na paginação: {e}")
            return []
        
    
    def get_active_loans_by_staff(self, staff_id):
        """Obtém a lista de empréstimos ativos de um funcionário."""
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT inventory_id, SUM(CASE WHEN type = 'OUT' THEN quantity ELSE -quantity END) as balance
                FROM movements
                WHERE staff_id = ?
                GROUP BY inventory_id
                HAVING balance > 0
            """, (staff_id,))
            
            active_loans = cur.fetchall()
            return active_loans

        except Exception as e:
            print(f"[X] Erro: {e}")
            return []
        
        
    def obter_categorias(self):
        """Obtém todas as categorias do banco de dados"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id, name FROM categories ORDER BY name")
            return cur.fetchall()
        except Exception as e:
            print(f"[X] Erro ao obter categorias: {e}")
            return []
    
    
    def get_recent_movements(self, limit=50):
        """Obtém as movimentações mais recentes do inventário."""
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT 
                    m.id,
                    m.inventory_id,
                    m.staff_id,
                    m.type,
                    m.quantity,
                    m.timestamp,
                    i.name as item_name,
                    i.serial_number,
                    s.name as staff_name
                FROM movements m
                INNER JOIN inventory i ON m.inventory_id = i.id
                INNER JOIN staff s ON m.staff_id = s.id
                ORDER BY m.timestamp DESC
                LIMIT ?
            """, (limit,))
            
            movements = cur.fetchall()
            return movements
            
        except Exception as e:
            print(f"[X] Erro ao buscar movimentações: {e}")
            return []
    
    
    def verifica_patrimonio_existe(self, serial_number):
        """
        NOVA IMPLEMENTAÇÃO: Verifica se já existe um item com este número de patrimônio.
        
        Args:
            serial_number (str): Número de patrimônio a verificar
            
        Returns:
            bool: True se já existe, False caso contrário
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM inventory WHERE serial_number = ?", (serial_number,))
            count = cur.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"[X] Erro ao verificar patrimônio: {e}")
            return False
    
    
    def buscar_item_por_patrimonio(self, serial_number):
        """
        NOVA IMPLEMENTAÇÃO: Busca informações completas de um item pelo patrimônio.
        
        Args:
            serial_number (str): Número de patrimônio
            
        Returns:
            tuple: Dados do item ou None se não encontrado
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT id, name, serial_number, category_id, location_id, quantity_available, min_stock
                FROM inventory 
                WHERE serial_number = ?
            """, (serial_number,))
            return cur.fetchone()
        except Exception as e:
            print(f"[X] Erro ao buscar item: {e}")
            return None
    
    
    def verificar_ultimo_emprestimo(self, serial_number):
        """
        NOVA IMPLEMENTAÇÃO: Verifica quem foi a última pessoa a pegar emprestado um item.
        
        Args:
            serial_number (str): Número de patrimônio
            
        Returns:
            str: Nome da pessoa que pegou emprestado ou None
        """
        try:
            cur = self.conn.cursor()
            # Busca o ID do item
            cur.execute("SELECT id FROM inventory WHERE serial_number = ?", (serial_number,))
            item = cur.fetchone()
            if not item:
                return None
            inventory_id = item[0]
            
            cur.execute("""
                SELECT s.name
                FROM movements m
                INNER JOIN staff s ON m.staff_id = s.id
                WHERE m.inventory_id = ? AND m.type = 'OUT'
                ORDER BY m.timestamp DESC
                LIMIT 1
            """, (inventory_id,))
            
            result = cur.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            print(f"[X] Erro ao verificar empréstimo: {e}")
            return None
    
    
    def deletar_categoria(self, categoria_id):
        """
        NOVA IMPLEMENTAÇÃO: Deleta uma categoria.
        
        Args:
            categoria_id (int): ID da categoria a deletar
            
        Returns:
            bool: True se deletou com sucesso, False caso contrário
        """
        try:
            cur = self.conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM inventory WHERE category_id = ?", (categoria_id,))
            count = cur.fetchone()[0]
            if count > 0:
                raise ValueError(f"Não é possível deletar. Existem {count} itens usando esta categoria.")
            
            cur.execute("DELETE FROM categories WHERE id = ?", (categoria_id,))
            self.conn.commit()
            print(f"[OK] Categoria ID {categoria_id} deletada.")
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro ao deletar categoria: {e}")
            raise
    
    
    def deletar_item(self, serial_number):
        """
        NOVA IMPLEMENTAÇÃO: Deleta um item do inventário.
        
        Args:
            serial_number (str): Número de patrimônio do item
            
        Returns:
            bool: True se deletou com sucesso, False caso contrário
        """
        try:
            cur = self.conn.cursor()
            
            cur.execute("SELECT id, quantity_available FROM inventory WHERE serial_number = ?", (serial_number,))
            item = cur.fetchone()
            
            if not item:
                raise ValueError("Item não encontrado.")
            
            inventory_id, qtd_disponivel = item
            if qtd_disponivel < 0:
                raise ValueError("Não é possível deletar. Item possui empréstimos ativos.")
            
            cur.execute("DELETE FROM movements WHERE inventory_id = ?", (inventory_id,))
            cur.execute("DELETE FROM inventory WHERE id = ?", (inventory_id,))
            
            self.conn.commit()
            print(f"[OK] Item {serial_number} deletado.")
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"[X] Erro ao deletar item: {e}")
            raise