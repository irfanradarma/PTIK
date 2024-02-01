import streamlit as st
import pandas as pd
import plotly.express as px

nilai = pd.read_csv("https://docs.google.com/spreadsheets/d/1Wb4eIqgBATGS8gOSa50le8j2-R7YI6KxARswHDufM6E/export?format=csv")
aut = pd.read_csv("https://docs.google.com/spreadsheets/d/1Wb4eIqgBATGS8gOSa50le8j2-R7YI6KxARswHDufM6E/export?format=csv&gid=1944478741")

def login(NPM, PASS, aut):
    password = aut[aut['NPM']==NPM]["PASS"].values[0]
    if str(password) == str(PASS):
        return "Benar"
    else:
        return "Salah"

def show_nilai(NPM, nilai):
    df = nilai[nilai["NPM"] == NPM]
    KELAS = df["KELAS"].values[0]
    RERATA = round(nilai[nilai["KELAS"] == KELAS]["NILAI_AKHIR"].mean(axis=0),2)
    NICK = df["NICK"].values[0]
    NILAI_AKHIR = df["NILAI_AKHIR"].values[0]
    df = df.drop(["NPM", "NAMA", "NICK", "KELAS", "NILAI_AKHIR"], axis=1)
    return NICK, NILAI_AKHIR, df, RERATA

def visualize(df):
    komposisi = df.values[0]
    label = df.columns

    # Create a DataFrame for plotly express
    data = pd.DataFrame({'Categories': label, 'Values': komposisi})

    # Create a bar chart using plotly express
    fig = px.bar(data, x='Categories', y='Values', text='Values', labels={'Values': 'Values'})

    # Customize the layout for mobile-friendly design
    fig.update_layout(
        xaxis_title='Komponen Nilai',
        yaxis_title='Nilai',
        title='Komposisi Nilai PTIK',
        showlegend=False,  # Hide legend for simplicity
        barmode='group',   # Choose 'group' or 'stack' as per your preference
        autosize=True,
        margin=dict(l=0, r=0, t=30, b=0),  # Adjust margins for better mobile display
    )
    return fig

def main():
    st.title("Nilai PTIK")
    
    # Login section
    st.subheader("Login")
    username = st.text_input("NPM:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        username = int(username)
        password = int(password)
        user_aut = login(username, password, aut)
        if user_aut == "Benar":
            st.success("Login Successful!")
            NICK, NILAI_AKHIR, KOMPOSISI, RERATA= show_nilai(username, nilai)
            st.subheader(f"Halo {NICK}!")
            st.write("Terima kasih sudah bekerja keras di kelas PTIK selama satu semester!")
            st.write("Semoga perjuanganmu tidak sia-sia, dan prestasimu semakin gemilang ke depan!")
            with st.container():
                st.write("Nilai akhir PTIK kamu adalah:")
                with st.expander("Nilai Akhir Kamu adalah:"):
                    st.header(NILAI_AKHIR)
                    st.write(f"nilai rata-rata kelas kamu adalah: {RERATA}")
                with st.expander("Komponen nilai akhir tersebut adalah:"):
                    fig = visualize(KOMPOSISI)
                    st.plotly_chart(fig)
                    st.write("Selamat yah!")
                    st.write("Semoga perjuangan kamu membuahkan hasil yang memuaskan")
        else:
            st.error("Password yang Anda masukkan salah!")

if __name__ == "__main__":
    main()
