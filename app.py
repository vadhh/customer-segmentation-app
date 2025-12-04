import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Customer Segmentation App", layout="wide")

@st.cache_resource
def load_assets():
    try:
        model = joblib.load('kmeans_model.joblib')
        scaler = joblib.load('scaler.joblib')
        try:
            data = pd.read_csv('cluster_data.csv')
        except:
            data = None
        return model, scaler, data
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None, None

model, scaler, df_display = load_assets()

st.sidebar.header("📝 Input Data Pelanggan")
st.sidebar.write("Masukkan perilaku belanja pelanggan:")

# Session state untuk menyimpan nilai input
if "total_qty" not in st.session_state:
    st.session_state.total_qty = 100
if "avg_unit_price" not in st.session_state:
    st.session_state.avg_unit_price = 12.5
if "avg_trx_value" not in st.session_state:
    st.session_state.avg_trx_value = 1500.0

# Fungsi untuk randomizer
def randomize_inputs():
    st.session_state.total_qty = np.random.randint(5, 2000) # Range disesuaikan dengan data asli
    st.session_state.avg_unit_price = round(np.random.uniform(5.0, 50.0), 2)
    st.session_state.avg_trx_value = round(np.random.uniform(300.0, 5000.0), 2)

# Tombol Randomizer
if st.sidebar.button("🎲 Randomizer Data", use_container_width=True):
    randomize_inputs()
    st.sidebar.success("Data telah dirandomisasi!")

st.sidebar.write("---")

# Input sesuai fitur di notebook (X)
total_qty = st.sidebar.number_input(
    "Total Quantity (Barang Dibeli)", 
    min_value=1, 
    value=st.session_state.total_qty,
    key="total_qty"
)
avg_unit_price = st.sidebar.number_input(
    "Rata-rata Harga Unit ($)", 
    min_value=0.0, 
    value=st.session_state.avg_unit_price,
    step=0.01,
    key="avg_unit_price"
)
avg_trx_value = st.sidebar.number_input(
    "Rata-rata Nilai Transaksi ($)", 
    min_value=0.0, 
    value=st.session_state.avg_trx_value,
    step=0.01,
    key="avg_trx_value"
)

# Tombol Prediksi
if st.sidebar.button("🔮 Prediksi Segmen", use_container_width=True):
    if model is not None and scaler is not None:
        
        new_data = np.array([[total_qty, avg_unit_price, avg_trx_value]])
        
        # Scaling data
        new_data_scaled = scaler.transform(new_data)
        
        # Prediksi Cluster
        cluster_pred = model.predict(new_data_scaled)[0]
        
        st.title("📊 Hasil Segmentasi Pelanggan")
        
        # Mapping Persona Sesuai Sprint 4
        # Cluster 0 -> Big Spender
        # Cluster 3 -> The Whales
        # Cluster 2 -> Quality Seekers
        # Cluster 1 -> Budget Shoppers
        
        personas = {
            0: {
                "name": "Big Spender", 
                "color": "#2ca02c", # Hijau
                "desc": "Pelanggan Sultan dengan nilai transaksi sangat tinggi. Sensitivitas harga rendah.", 
                "action": "👑 **Strategi:** Layanan Prioritas, Cross-sell produk eksklusif, Concierge Service."
            },
            3: {
                "name": "The Whales", 
                "color": "#1f77b4", # Biru
                "desc": "Membeli dalam jumlah (Quantity) sangat masif namun harga unit rendah. Reseller/B2B.", 
                "action": "📦 **Strategi:** Diskon Grosir (Bulk Discount), Paket Bundling Besar, Program Loyalitas B2B."
            },
            2: {
                "name": "Quality Seekers", 
                "color": "#ff7f0e", # Oranye
                "desc": "Membeli barang dengan harga satuan tinggi (kualitas bagus), namun jumlahnya tidak banyak.", 
                "action": "💎 **Strategi:** Product Bundling Premium, Tawarkan produk 'Limited Edition' atau New Arrivals."
            },
            1: {
                "name": "Budget Shoppers", 
                "color": "#d62728", # Merah
                "desc": "Transaksi kecil, harga barang murah, dan quantity sedikit. Sangat sensitif harga.", 
                "action": "🏷️ **Strategi:** Voucher Minimum Belanja (untuk menaikkan Basket Size), Flash Sale, Diskon Ongkir."
            }
        }
        
        persona = personas.get(cluster_pred, {"name": f"Cluster {cluster_pred}", "desc": "Tipe pelanggan tidak dikenal.", "action": "Analisis lebih lanjut."})

        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: {persona.get('color', '#f0f2f6')}; color: white;">
            <h2 style="margin:0;">{persona['name']}</h2>
            <p style="font-size: 18px;">{persona['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Spacer
        st.info(persona['action'])

        strategies = {
            0: '''
**Ringkasan:** Pelanggan dengan nilai transaksi sangat tinggi. Sensitivitas harga rendah; fokus pada pengalaman dan eksklusivitas.

**Taktik Jangka Pendek:**
- Penawaran eksklusif (early access, limited bundles).
- Personalized recommendations dan cross-sell di checkout.

**Taktik Jangka Panjang:**
- Loyalty tiers dengan benefit nyata (free expedited shipping, dedicated support).
- Program retensi VIP dan subscription premium.

**Komunikasi & Channel:**
- Email personal, notifikasi in-app, account manager untuk high-value customers.

**KPI Utama:** AOV, CLTV, repeat purchase rate, churn rate.

**Contoh Kampanye:** "VIP Preview + White-Glove Delivery" (early access + layanan pengiriman premium).
''',
            3: '''
**Ringkasan:** Pembeli volume besar (B2B / reseller). Harga per unit rendah, total order value tinggi.

**Taktik Jangka Pendek:**
- Tiered volume discounts dan paket grosir.
- Opsi checkout B2B (invoice, tax forms).

**Taktik Jangka Panjang:**
- Portal B2B, kontrak harga negosiasi, dedicated account manager.
- Integrasi ERP / purchase order untuk pelanggan besar.

**Komunikasi & Channel:**
- Sales outreach, email bisnis, katalog harga khusus.

**KPI Utama:** Units per order, repeat order frequency, margin per bulk order.

**Contoh Kampanye:** "Tiered Volume Discount + Dedicated B2B Account".
''',
            2: '''
**Ringkasan:** Pembeli produk bernilai tinggi per unit; mengutamakan kualitas dan fitur.

**Taktik Jangka Pendek:**
- Highlight product benefits (reviews, demo, UGC).
- Tawaran bundle premium dan free trials / warranty extension.

**Taktik Jangka Panjang:**
- Program loyalitas untuk pembelian premium, membership dengan benefit.

**Komunikasi & Channel:**
- Content marketing, influencer, targeted email berbasis interest.

**KPI Utama:** Conversion rate pada produk premium, AOV, margin.

**Contoh Kampanye:** "Premium Bundle + Extended Warranty".
''',
            1: '''
**Ringkasan:** Price-sensitive buyer; transaksi dan harga rendah, responsif terhadap diskon.

**Taktik Jangka Pendek:**
- Coupon/discount targeted, free-shipping-threshold, flash sale.
- Bundle murah untuk meningkatkan basket size.

**Taktik Jangka Panjang:**
- Program loyalitas yang mempercepat rewards untuk pembelian kecil.
- Retargeting dengan personalized vouchers dan referral incentives.

**Komunikasi & Channel:**
- Promo-driven emails, push notifications, social ads bertarget diskon.

**KPI Utama:** Conversion rate, average basket size, coupon redemption rate, repeat frequency.

**Contoh Kampanye:** "Buy 2 Get 1 / 10% off with Min Spend".
'''
        }

        strategy_text = strategies.get(cluster_pred, "Strategi tidak tersedia untuk cluster ini.")

        with st.expander(f"Strategi Lengkap — {persona['name']}"):
            st.markdown(strategy_text)

        st.markdown("---")
        st.subheader("📍 Posisi Pelanggan dalam Peta Sebaran")
        
        if df_display is not None:
            if 'Persona' not in df_display.columns:
                 # Mapping numeric cluster ke nama persona
                 persona_map = {k: v['name'] for k, v in personas.items()}
                 df_display['Persona'] = df_display['Cluster'].map(persona_map)
            
            fig = px.scatter_3d(
                df_display,
                x='TotalQuantity',
                y='AvgTransactionValue',
                z='AvgUnitPrice',
                color='Persona',
                opacity=0.3, # Buat titik lain agak transparan
                title="Visualisasi 3D Cluster Pelanggan",
                color_discrete_map={
                    "Big Spender": "#2ca02c",
                    "The Whales": "#1f77b4",
                    "Quality Seekers": "#ff7f0e",
                    "Budget Shoppers": "#d62728"
                }
            )
            
            fig.add_scatter3d(
                x=[total_qty],
                y=[avg_trx_value],
                z=[avg_unit_price],
                mode='markers',
                marker=dict(size=20, color='black', symbol='x'),
                name='Pelanggan Baru (Input)'
            )
            
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=40),
                scene=dict(
                    xaxis_title='Total Qty',
                    yaxis_title='Trx Value',
                    zaxis_title='Unit Price'
                ),
                legend=dict(yanchor="top", y=0.9, xanchor="left", x=0.1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Data visualisasi (cluster_data.csv) tidak ditemukan. Pastikan file tersebut ada di folder yang sama.")

    else:
        st.error("Model atau Scaler belum dimuat. Pastikan file .joblib ada di folder yang sama.")

else:
    st.title("👋 Selamat Datang di Dashboard Segmentasi")
    "**Tim Capstone Project	: A25-CS286**"
    st.markdown("""
    Aplikasi ini menggunakan Machine Learning (**K-Means Clustering**) untuk mengelompokkan pelanggan menjadi 4 Persona:
    
    1.  **Big Spender**     : Nilai transaksi tinggi.
    2.  **The Whales**      : Volume pembelian massal.
    3.  **Quaility Seekers**: Membeli barang-barang mahal/berkualitas.
    4.  **Budget Shoppers** : Pembeli hemat/budget.
    
    👈 **Silakan masukkan data transaksi di panel sebelah kiri untuk memulai prediksi.**
    """)
    
    if df_display is not None:
        st.write("### Data Pelanggan Saat Ini (Sampel)")
        st.dataframe(df_display.head(10))