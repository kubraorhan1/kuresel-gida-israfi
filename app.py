import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Gıda İsrafı Analizi", layout="wide")

# --- Başlık ve Açıklama ---
st.title("🌍 Gıda İsrafı: Küresel Bir Sorun")
st.markdown("""
Gıda israfı; ekonomik, çevresel ve etik boyutlarıyla günümüzde en kritik sorunlardan biridir. 
Bu uygulama ile ülkelerin israf verilerini analiz edebilir, stratejik öneriler geliştirebilir ve kendi israf durumunuzu görebilirsiniz.
""")

# --- Örnek Veri Seti ---
data = pd.DataFrame({
    "Ülke": ["Türkiye", "ABD", "Almanya", "Fransa", "Hindistan"],
    "Kişi Başı İsraf (kg)": [93, 120, 85, 95, 50],
    "Toplam İsraf (milyon ton)": [7.7, 40, 7.2, 6.3, 68],
    "Ekonomik Kayıp (milyar $)": [14, 160, 20, 18, 70]
})

# --- 2. Bölüm: Ülkeye Göre Özet ---
st.header("📊 Ülkelere Göre Gıda İsraf Özeti")
st.dataframe(data, use_container_width=True)

# --- 3. Bölüm: Stratejik Yorum ve Model Değerlendirme ---
st.header("📌 Model Değerlendirme & Stratejik Yorum")
st.markdown("""
Yukarıdaki verilere göre gelişmiş ülkelerde kişi başına israf oranı yüksekken, gelişmekte olan ülkelerde **toplam israf miktarı** daha yüksektir. 
Bu durum, tüketim alışkanlıkları ve nüfus büyüklüğü ile ilişkilidir. Stratejik önlemler:
- **Farkındalık kampanyaları** ile bireysel israf azaltılabilir.
- **Lojistik altyapılar** iyileştirilerek tarladan sofraya süreç optimize edilebilir.
- **Yasal düzenlemeler** ile market ve restoranların fazla ürünleri bağışlaması teşvik edilmelidir.
""")

# --- 4. Bölüm: Ana Grafik ---
st.header("📈 Gıda İsrafı Karşılaştırması")
selected_metric = st.selectbox("Görüntülemek istediğiniz metrik:",
                               ["Kişi Başı İsraf (kg)", "Toplam İsraf (milyon ton)", "Ekonomik Kayıp (milyar $)"])

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="Ülke", y=selected_metric, data=data, palette="coolwarm", ax=ax)
plt.title(f"{selected_metric} Karşılaştırması")
plt.xlabel("Ülke")
plt.ylabel(selected_metric)
plt.xticks(rotation=45)
st.pyplot(fig)

# --- 5. Bölüm: Kullanıcıdan Veri Al ve Seçim ---
st.sidebar.header("🧮 Kendi İsraf Verilerinizi Girin ve Tahmin Edin")

user_country = st.sidebar.text_input("Ülke Adı", "Senin Ülken")
user_population = st.sidebar.number_input("Nüfus (milyon)", min_value=1.0, max_value=2000.0, value=85.0)
user_waste_per_person = st.sidebar.number_input("Kişi Başı Gıda İsrafı (kg)", min_value=1.0, max_value=200.0,
                                                value=90.0)
user_economic_loss = st.sidebar.number_input("Ekonomik Kayıp (milyar $)", min_value=0.0, max_value=1000.0, value=15.0)

# Kullanıcı verileri dataframe
user_data = pd.DataFrame({
    "Ülke": [user_country],
    "Kişi Başı İsraf (kg)": [user_waste_per_person],
    "Toplam İsraf (milyon ton)": [(user_population * user_waste_per_person) / 1000],  # milyon ton
    "Ekonomik Kayıp (milyar $)": [user_economic_loss]
})

# Kullanıcıdan hangi ülkeyi grafik olarak görmek istediğini seçtir
st.sidebar.header("📊 Tahmin Edilecek Ülkeyi Seçin")
country_to_plot = st.sidebar.selectbox("Ülke Seçimi", options=[user_country])

plot_button = st.sidebar.button("Tahmini Veriyi Grafikle")

if plot_button:
    st.subheader(f"📍 {country_to_plot} için Tahmini Gıda İsrafı Verileri")

    # Seçilen metriklerin grafiklerini gösterelim (dikey bar şeklinde)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    user_data_melted = user_data.melt(id_vars="Ülke", var_name="Metrik", value_name="Değer")
    sns.barplot(x="Metrik", y="Değer", data=user_data_melted, palette="viridis", ax=ax2)
    ax2.set_title(f"{country_to_plot} - Tahmini Gıda İsrafı Metrikleri")
    ax2.set_xlabel("")
    ax2.set_ylabel("Değer")
    st.pyplot(fig2)
