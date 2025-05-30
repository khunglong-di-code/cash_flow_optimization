import csv
import random
import uuid
import math 

NUM_PEOPLE = 20
NUM_EVENTS = 5000
FILENAME = "cash_flow_optimization_dataset.csv" 

PERSON_IDS = [f"Person_{i+1}" for i in range(NUM_PEOPLE)]

EXPENSE_DESCRIPTIONS = [
    "Ăn trưa chung", "Cà phê nhóm", "Mua đồ dùng văn phòng", "Vé xem phim",
    "Tiền điện nước chia sẻ", "Tiệc cuối tuần", "Đồ ăn vặt cho nhóm",
    "Sách và tài liệu chung", "Đi lại chung (taxi/grab)", "Quà tặng chung",
    "Thực phẩm cho bữa tối chung", "Đăng ký dịch vụ trực tuyến dùng chung",
    "Hoạt động team building", "Thiết bị nhỏ cho dự án", "Đồ dùng sinh hoạt chung"
]

def generate_dataset_divisible_cost(num_events, person_ids, descriptions, filename):
    header = ["event_id", "description", "total_cost", "paid_by", "participants"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        for i in range(num_events):
            event_id = uuid.uuid4()
            description = random.choice(descriptions)
            num_participants = random.randint(2, len(person_ids))
            current_participants_ids = random.sample(person_ids, num_participants)
            paid_by_person = random.choice(current_participants_ids)
            initial_total_cost_raw = random.uniform(50000, 2000000)
            initial_total_cost_int = round(initial_total_cost_raw / 1000) * 1000 
            cost_per_participant_approx = round(initial_total_cost_int / num_participants)
            adjusted_total_cost = cost_per_participant_approx * num_participants
            if adjusted_total_cost < num_participants and initial_total_cost_int > 0:
                 adjusted_total_cost = num_participants * (round(initial_total_cost_int/num_participants) if round(initial_total_cost_int/num_participants) > 0 else 1)
            participants_str = ";".join(current_participants_ids)
            writer.writerow([
                event_id,
                description,
                int(adjusted_total_cost), 
                paid_by_person,
                participants_str
            ])
            
    print(f"Dataset '{filename}' với {num_events} dòng đã được tạo thành công cho {len(person_ids)} người.")
    print("Lưu ý: total_cost đã được điều chỉnh để chia hết cho số người tham gia.")
    
if __name__ == "__main__":
    generate_dataset_divisible_cost(NUM_EVENTS, PERSON_IDS, EXPENSE_DESCRIPTIONS, FILENAME)