import random
from locust import HttpUser, TaskSet, task, between

#  "CHỈ XEM" 
class ReadOnlyTasks(TaskSet):
    """
    Kịch bản API Backend: Mô phỏng user chỉ lướt xem.
    """
    @task
    def view_boards_and_cards_flow(self):
        # Lấy tất cả các boards
        board_id_list = []
        with self.client.get(
            "/boards", 
            name="/boards (GET all)",
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure("Failed to get all boards")
                return 
            try:
                boards = response.json().get("data", [])
                if not boards:
                    response.failure("No boards found")
                    return 
                board_id_list = [b.get("id") for b in boards if b.get("id")]
            except Exception as e:
                response.failure(f"Bad JSON response from /boards: {e}")
                return

        if not board_id_list:
            return 

        random_board_id = random.choice(board_id_list)
        self.wait() 

        # Lấy tất cả card của 1 board
        card_id_list = []
        with self.client.get(
            f"/cards/board/{random_board_id}", 
            name="/cards/board/[boardId]", 
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(f"Failed to get cards for board {random_board_id}")
                return
            try:
                cards = response.json().get("data", [])
                if not cards:
                    return 
                card_id_list = [c.get("id") for c in cards if c.get("id")]
            except Exception as e:
                response.failure(f"Bad JSON from /cards/board: {e}")
                return

        if not card_id_list:
            return 

        random_card_id = random.choice(card_id_list)
        self.wait()
        
        # Lấy chi tiết 1 card
        self.client.get(
            f"/cards/{random_card_id}", 
            name="/cards/[id] (GET one)"
        )


#  "CHỈNH SỬA" 
class ReadWriteTasks(TaskSet):
    """
    Kịch bản API Backend: Mô phỏng user "nặng" - tạo, sửa, xóa dữ liệu.
    """
    @task
    def create_update_delete_card_flow(self):
        # TỰ ĐỘNG LẤY BOARD ID
        board_id_list = []
        with self.client.get(
            "/boards", 
            name="/boards (GET for WriteTask)",
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure("Failed to get boards (for WriteTask)")
                return 
            try:
                boards = response.json().get("data", [])
                if not boards:
                    response.failure("No boards found (for WriteTask)")
                    return 
                board_id_list = [b.get("id") for b in boards if b.get("id")]
            except Exception as e:
                response.failure(f"Bad JSON from /boards (for WriteTask): {e}")
                return

        if not board_id_list:
            return

        selected_board_id = random.choice(board_id_list)
        
        # TẠO CARD MỚI
        new_card_data = {
            "boardId": selected_board_id,
            "content": f"Locust Test Card - {random.randint(100, 999)}",
            "order": 1,
            "subjectName": "Locust Automated Test", 
            "semester": "HK1 2025-2026",
            "typeSubject": "Lý thuyết"
        }
        
        created_card_id = None
        
        with self.client.post(
            "/cards",
            json=new_card_data,
            name="/cards (POST create)",
            catch_response=True
        ) as response:
            if not response.ok:
                response.failure(f"Failed to create card: {response.status_code}")
                return
            try:
                created_card_id = response.json().get("data", {}).get("id")
            except Exception as e:
                response.failure(f"Bad JSON on POST /cards: {e}")
                return

        if not created_card_id:
            response.failure("Created card ID not found in response")
            return

        self.wait_time = between(2, 5)
        self.wait()
        
        # CẬP NHẬT CARD VỪA TẠO
        update_data = { "description": "Mô tả được cập nhật tự động bởi Locust." }
        self.client.put(
            f"/cards/{created_card_id}",
            json=update_data,
            name="/cards/[id] (PUT update)"
        )
        
        self.wait_time = between(2, 5)
        self.wait()
        
        # XÓA CARD VỪA TẠO 
        self.client.delete(
            f"/cards/{created_card_id}",
            name="/cards/[id] (DELETE)"
        )



# USER 1: NGƯỜI DÙNG FRONTEND 
class FrontendUser(HttpUser):
    """
    Loại user này chỉ đánh vào FRONTEND.
    Sẽ chiếm 1/4 (25%) tổng số user.
    """
    
    host = "http://172.188.200.212"
    
    # Tỷ lệ: 1 (so với 3 của BackendUser)
    weight = 1 
    
    wait_time = between(1, 5) # Chờ 1-5 giây

    @task
    def load_homepage(self):
        """Tác vụ 1: Truy cập trang chủ"""
        self.client.get(
            "/",
            name="/ (Frontend Homepage)"
        )



# USER 2: NGƯỜI DÙNG BACKEND
class BackendUser(HttpUser):
    """
    Loại user này chỉ đánh vào BACKEND (API).
    Sẽ chiếm 3/4 (75%) tổng số user.
    """
    
    host = "http://135.171.146.68"
    
    # Tỷ lệ: 3 (so với 1 của FrontendUser)
    weight = 3 
    
    wait_time = between(1, 3) 

    # Phân bổ tỷ lệ hành vi (cho riêng user backend):
    tasks = {
        ReadOnlyTasks: 4,  # 80% user backend sẽ chỉ xem
        ReadWriteTasks: 1  # 20% user backend sẽ chỉnh sửa
    }