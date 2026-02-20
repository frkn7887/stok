Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import streamlit as st
import pandas as pd
import datetime
import os
import io

# --- KULLANICI BİLGİLERİ (Burayı dilediğin gibi çoğaltabilirsin) ---
USER_CREDENTIALS = {
    "admin": "sifre123",
    "mudur": "depo2024",
    "operator": "isletme78"
}

def check_password():
    """Kullanıcı adı ve şifre kontrolü yapar."""
    def password_entered():
        if st.session_state["username"] in USER_CREDENTIALS and \
           st.session_state["password"] == USER_CREDENTIALS[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Şifreyi bellekten sil
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 Stok Takip Sistemi Girişi")
        st.text_input("Kullanıcı Adı", key="username")
        st.text_input("Parola", type="password", key="password")
        st.button("Giriş Yap", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Kullanıcı adı veya şifre hatalı!")
        st.text_input("Kullanıcı Adı", key="username")
        st.text_input("Parola", type="password", key="password")
        st.button("Giriş Yap", on_click=password_entered)
        return False
    else:
        return True

if check_password():
    # --- PROGRAMIN ANA GÖVDESİ BURADAN BAŞLIYOR ---
    DB_FILE = 'stok_bulut_verisi.csv'

    def load_data():
        if os.path.exists(DB_FILE):
            return pd.read_csv(DB_FILE)
        return pd.DataFrame(columns=[
            'ID', 'Gelen Ürün İsmi', 'Döküm No', 'Lokasyon', 
            'Gelen Yarı Mamul (Adet)', 'İşlenen Yarı Mamul (Adet)', 
            'Kalan Adet', 'Kampanya', 'Giriş Tarihi'
        ])

    def save_data(df):
        df.to_csv(DB_FILE, index=False)

    st.set_page_config(page_title="Global Üretim Takip", layout="wide")
    st.sidebar.success(f"Hoş geldin, {st.session_state['username']}")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["password_correct"] = False
...         st.rerun()
... 
...     st.title("🌍 Global Yarı Mamul ve Stok Takip Sistemi")
...     import streamlit as st
... import pandas as pd
... import datetime
... import os
... import io
... 
... DB_FILE = 'stok_uretim_verisi.csv'
... 
... # Depo Lokasyon Listesi
... DEPO_ALANLARI = [
...     "YH 10 K. A", "YH 10 ORTA", "YH 10 D. D", "YH 11 K. A", "YH 11 D. D", "YH 11 ORTA",
...     "YH 12 K. A", "YH 12 ORTA", "YH 12 D. D", "YH 13 K. A", "YH 13 ORTA", "YH 13 D. D",
...     "YH 14 K. A", "YH 14 ORTA", "YH 14 D. D", "YH 15 K. A", "YH 15 ORTA", "YH 15 D. D",
...     "YH 16 K. A", "YH 16 ORTA", "YH 16 D. D", "EH 7 K. A", "EH 7 ORTA", "EH 7 D. D",
...     "EH 8 K. A", "EH 8 ORTA", "EH 8 D. D", "EH 9 K. A", "EH 9 ORTA", "EH 9 D. D",
...     "EH 10 K. A", "EH 10 ORTA", "EH 10 D. D", "EH 11 K. A", "EH 11 ORTA", "EH 11 D. D",
...     "EH 12 K. A", "EH 12 ORTA", "EH 12 D. D", "EH 13 K. A", "EH 13 ORTA", "EH 13 D. D",
...     "EH 14 K. A", "EH 14 ORTA", "EH 14 D. D", "EH 15 K. A", "EH 15 ORTA", "EH 15 D. D",
...     "EH 16 K. A", "EH 16 ORTA", "EH 16 D. D", "EH 17 K. A", "EH 17 ORTA", "EH 17 DİREK DİBİ"
... ]
... 
... def load_data():
...     if os.path.exists(DB_FILE):
...         return pd.read_csv(DB_FILE)
...     return pd.DataFrame(columns=[
...         'ID', 'Gelen Ürün İsmi', 'Döküm No', 'Lokasyon', 
...         'Gelen Yarı Mamul (Adet)', 'İşlenen Yarı Mamul (Adet)', 
...         'Kalan Adet', 'Kampanya', 'Giriş Tarihi'
...     ])
... 
... def save_data(df):
...     df.to_csv(DB_FILE, index=False)
... 
... # Excel'e dönüştürme fonksiyonu
... def to_excel(df):
...     output = io.BytesIO()
...     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
...         df.to_excel(writer, index=False, sheet_name='Stok Raporu')
...     return output.getvalue()

st.set_page_config(page_title="Üretim Stok Takip", layout="wide")
st.title("🏭 Yarı Mamul İşleme ve Stok Takip")

df = load_data()

# --- YAN PANEL: GİRİŞ ---
st.sidebar.header("📥 Yeni Yarı Mamul Girişi")
with st.sidebar.form("giris_formu"):
    urunler = ["Beam Blank", "Kütük", "Ray", "400x500", "Diğer"]
    u_adi = st.selectbox("Gelen Ürün İsmi", urunler)
    if u_adi == "Diğer": u_adi = st.text_input("Ürün İsmi")
    
    dokum = st.text_input("Döküm Numarası")
    lokasyon = st.selectbox("Depo Alanı", DEPO_ALAN_ALARI if 'DEPO_ALAN_ALARI' in locals() else DEPO_ALANLARI)
    adet = st.number_input("Gelen Yarı Mamul (Adet)", min_value=1, step=1)
    kampanya = st.text_input("Kampanya")
    tarih = st.date_input("Giriş Tarihi", datetime.date.today())
    
    if st.form_submit_button("Sisteme İşle"):
        yeni_id = df['ID'].max() + 1 if not df.empty else 1
        yeni_satir = {
            'ID': yeni_id, 'Gelen Ürün İsmi': u_adi, 'Döküm No': dokum, 
            'Lokasyon': lokasyon, 'Gelen Yarı Mamul (Adet)': adet, 
            'İşlenen Yarı Mamul (Adet)': 0, 'Kalan Adet': adet, 
            'Kampanya': kampanya, 'Giriş Tarihi': tarih
        }
        df = pd.concat([df, pd.DataFrame([yeni_satir])], ignore_index=True)
        save_data(df)
        st.rerun()

# --- ANA EKRAN ---
c1, c2, c3 = st.columns(3)
with c1: st.metric("Toplam Gelen", f"{df['Gelen Yarı Mamul (Adet)'].sum()} Adet")
with c2: st.metric("Toplam İşlenen", f"{df['İşlenen Yarı Mamul (Adet)'].sum()} Adet")
with c3: st.metric("Mevcut Stok", f"{df['Kalan Adet'].sum()} Adet")

st.subheader("📋 Güncel Stok ve Konum Listesi")
search = st.text_input("🔍 Döküm No veya Konum Ara...")
view_df = df[df.astype(str).apply(lambda x: search.lower() in x.str.lower().values, axis=1)] if search else df
st.dataframe(view_df, use_container_width=True)

# --- İŞLEME VE RAPORLAMA ---
st.divider()
col_islem, col_rapor = st.columns([2, 1])

with col_islem:
    st.subheader("⚙️ Yarı Mamul İşleme")
    id_sec = st.number_input("İşlem Yapılacak Kayıt ID", min_value=1, step=1)
    mik_sec = st.number_input("İşlenen Adet", min_value=1, step=1)
    if st.button("İşlemeyi Onayla"):
        if id_sec in df['ID'].values:
            idx = df.index[df['ID'] == id_sec][0]
            if mik_sec <= df.at[idx, 'Kalan Adet']:
                df.at[idx, 'İşlenen Yarı Mamul (Adet)'] += mik_sec
                df.at[idx, 'Kalan Adet'] -= mik_sec
                save_data(df)
                st.success("Stok güncellendi.")
                st.rerun()
            else: st.error("Stok yetersiz!")

with col_rapor:
    st.subheader("💾 Raporlama")
    excel_data = to_excel(df)
    st.download_button(
        label="📥 Excel Raporu İndir",
        data=excel_data,
        file_name=f'stok_raporu_{datetime.date.today()}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    if st.button("Sevk Edilenleri Temizle"):
        # Kalan adedi 0 olanları arşivlemek/silmek istersen
        df = df[df['Kalan Adet'] > 0]
        save_data(df)
        st.warning("Stokta kalmayan ürünler listeden kaldırıldı.")
        st.rerun()
    # (Önceki yazdığımız tüm stok, lokasyon ve raporlama kodları burada devam eder...)
    # [Buraya önceki yanıttaki tablo ve işlem kodlarını ekleyebilirsin]
    
    df = load_data()
