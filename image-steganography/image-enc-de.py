from PIL import Image
import numpy as np
#hevorix
def encode_into_existing_image(py_file, jpg_file, output_file):
    with open(py_file, 'rb') as f:
        file_data = f.read()
    
    if not file_data:
        raise ValueError(f"Fayl '{py_file}' bo'sh yoki o'qib bo'lmaydi!")
    
    image = Image.open(jpg_file)
    image_array = np.array(image)
    
    if len(image_array.shape) < 3 or image_array.shape[2] < 3:
        raise ValueError(f"Rasm '{jpg_file}' haqiqiy rangli tasvir emas (RGB talab qilinadi)!")
    
    pixel_count = image_array.shape[0] * image_array.shape[1]
    print(f"Asl rasm piksel soni: {pixel_count}")
    print(f"Yashiriladigan fayl hajmi: {len(file_data)} bayt")
   
    flat_image = image_array.flatten()
    file_data = np.frombuffer(file_data, dtype=np.uint8)
    if len(file_data) * 8 > len(flat_image):
        raise ValueError("Yashiriladigan ma'lumot rasm hajmidan katta!")
    
    for i, byte in enumerate(file_data):
        for bit in range(8):
            flat_image[i * 8 + bit] = (flat_image[i * 8 + bit] & 0xFE) | ((byte >> (7 - bit)) & 1)

    new_image_array = flat_image.reshape(image_array.shape)
    new_image = Image.fromarray(new_image_array, mode='RGB')
    new_image.save(output_file)

    print(f"Fayl '{py_file}' '{jpg_file}' ichiga yashirildi va '{output_file}' nomi bilan saqlandi!")
    print(f"Yashirilgan fayl hajmi: {len(file_data)} bayt")

def decode_from_existing_image(jpg_file, output_py_file):
    image = Image.open(jpg_file)
    image_array = np.array(image)

    pixel_count = image_array.shape[0] * image_array.shape[1]
    print(f"Asl rasm piksel soni: {pixel_count}")

    flat_image = image_array.flatten()
    hidden_bits = []
    for i in range(len(flat_image)):
        hidden_bits.append(flat_image[i] & 1)
        if len(hidden_bits) % 8 == 0 and all(b == 0 for b in hidden_bits[-8:]):
            break
    
    byte_array = np.packbits(hidden_bits[:-8])
    with open(output_py_file, 'wb') as f:
        f.write(byte_array.tobytes())
    
    print(f"Rasmdan yashirilgan fayl '{output_py_file}' nomi bilan tiklandi!")
    print(f"Chiqib olingan fayl hajmi: {len(byte_array)} bayt")

menu_tanlash = input("Menulardan birini tanlang:\n1. Faylni mavjud rasm ichiga yashirish\n2. Rasmdan yashirilgan faylni chiqarish\n>>> ")
if menu_tanlash == "1":
    input_file = input("Yashirish kerak bo'lgan faylni kiriting (.txt, .py, .csv): ")
    existing_image = input("Mavjud rasmni kiriting (.png yoki .jpg): ")
    output_image = input("Yashirilgan ma'lumotli rasmni saqlash nomi (.png yoki .jpg): ")
    encode_into_existing_image(input_file, existing_image, output_image)
elif menu_tanlash == "2":
    encoded_image = input("Yashirilgan rasmni kiriting (.png yoki .jpg): ")
    output_file = input("Chiqadigan fayl nomi (.txt, .py, .csv): ")
    decode_from_existing_image(encoded_image, output_file)
else:
    print("Noto'g'ri tanlov! Faqat 1 yoki 2-ni tanlang.")
