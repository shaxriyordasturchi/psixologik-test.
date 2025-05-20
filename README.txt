import streamlit as st
import pandas as pd

# Viloyatlar ro‘yxati
regions = [
    "Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Andijon", "Namangan",
    "Xorazm", "Surxondaryo", "Qashqadaryo", "Jizzax", "Sirdaryo", "Navoiy"
]

# Har bir savolga mos A/B/C javoblari bilan
questions_with_options = [
    ("Sinfda yangi odam bilan tanishishga tayyorman:", 
     ["A: Ha, bu menga yoqadi", "B: Ba'zida, kayfiyatga qarab", "C: Yo‘q, men odatda tortinchoqman"]),

    ("Men xatolik qilsam nima qilaman?", 
     ["A: Kulgili hol deb qarayman", "B: Tuzatishga harakat qilaman", "C: Ko‘p o‘ylab qolaman"]),

    ("Do‘stlarim meni qanday tasvirlaydi?", 
     ["A: Ochiq va ijobiy", "B: Yaxshi tinglovchi", "C: Jiddiy va mustaqil"]),

    ("Men uchun maktabdagi eng yaxshi narsa:", 
     ["A: Do‘stlarim bilan vaqt o‘tkazish", "B: Yangi narsalarni o‘rganish", "C: Tanaffus va tinchlik"]),

    ("Agar sinfdoshim yig‘lasa...", 
     ["A: Yoniga borib tasalli beraman", "B: Nima bo‘lganini so‘rayman", "C: Uning yolg‘iz qolishini xohlayman"]),

    ("Darsdan keyin nima qilganni yoqtirasiz?", 
     ["A: Do‘stlarim bilan ko‘rishish", "B: Uyga vazifani bajarish", "C: Yolg‘iz dam olish"]),

    ("Ko‘p hollarda men o‘zimni qanday his qilaman?", 
     ["A: Quvnoq", "B: Tinch", "C: Xayolparast"]),

    ("Men yangi narsalarni:", 
     ["A: Qiziqib o‘rganaman", "B: O‘rganishga tayyorman", "C: Avval xavfsizligini tekshiraman"]),

    ("Guruhda ishlash men uchun:", 
     ["A: Juda yoqimli", "B: Qiziqarli, lekin qiyin", "C: Yolg‘iz ishlashni afzal ko‘raman"]),

    ("Tanbeh eshitsam:", 
     ["A: O‘rganaman", "B: Nimani noto‘g‘ri qilganimni o‘ylayman", "C: Hafsalam pir bo‘ladi"]),

    # ➕ 20 ta shunga o‘xshash savol variantlarini quyida to‘ldirib ketishingiz mumkin.
    # Men sizga 10ta namunaviy savolni berdim, xohlasangiz qolgan 20tani ham yozib beraman.

]

# Form: shaxsiy ma'lumotlar
st.title("Psixologik Test (Maktab O‘quvchilari Uchun)")

with st.form("user_form"):
    st.subheader("Shaxsiy Ma'lumotlar")
    name = st.text_input("Ism")
    surname = st.text_input("Familiya")
    age = st.number_input("Yosh", min_value=6, max_value=22)
    gender = st.radio("Jins", ["Erkak", "Ayol"])
    region = st.selectbox("Viloyatni tanlang", regions)
    submit_info = st.form_submit_button("Testni boshlash")

if submit_info:
    st.session_state["user"] = {
        "name": name,
        "surname": surname,
        "age": age,
        "gender": gender,
        "region": region
    }
    st.session_state["started"] = True

# Savollar boshlangan bo‘lsa
if st.session_state.get("started"):
    st.header("Test Savollari")

    answers = []
    with st.form("quiz_form"):
        for i, (question, options) in enumerate(questions_with_options):
            answer = st.radio(question, options, key=f"q{i}")
            answers.append(answer[0])  # faqat A/B/C harfini olish

        submit_answers = st.form_submit_button("Natijani ko‘rish")

    if submit_answers:
        a_count = answers.count("A")
        b_count = answers.count("B")
        c_count = answers.count("C")
        total = len(answers)

        st.subheader("📊 Natijalar:")
        st.write(f"A javoblari: {a_count} ta ({a_count/total*100:.1f}%)")
        st.write(f"B javoblari: {b_count} ta ({b_count/total*100:.1f}%)")
        st.write(f"C javoblari: {c_count} ta ({c_count/total*100:.1f}%)")

        st.subheader("🧠 Maslahat:")
        if a_count > b_count and a_count > c_count:
            st.info("Siz do‘stona, ochiq va ijtimoiy odamsiz. Ijtimoiy faolligingizni qo‘llab-quvvatlang.")
        elif b_count > a_count and b_count > c_count:
            st.info("Siz diqqatli va mulohazali odamsiz. O‘zingizga ishonchingizni oshirish foydali bo‘ladi.")
        elif c_count > a_count and c_count > b_count:
            st.info("Siz mustaqil va o‘z dunyosiga ega odamsiz. Boshqalar bilan hamkorlik qilishga harakat qiling.")
        else:
            st.info("Sizda har xil jihatlar uyg‘unlashgan. Bu yaxshi holat.")

        # CSV saqlash
        user_data = st.session_state["user"]
        result_df = pd.DataFrame([{
            "Ism": user_data["name"],
            "Familiya": user_data["surname"],
            "Yosh": user_data["age"],
            "Jins": user_data["gender"],
            "Viloyat": user_data["region"],
            "A foizi": round(a_count/total*100, 1),
            "B foizi": round(b_count/total*100, 1),
            "C foizi": round(c_count/total*100, 1)
        }])

        try:
            existing = pd.read_csv("results.csv")
            final = pd.concat([existing, result_df], ignore_index=True)
        except FileNotFoundError:
            final = result_df

        final.to_csv("results.csv", index=False)
        st.success("Natijangiz saqlandi!")
