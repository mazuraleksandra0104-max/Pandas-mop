import streamlit as st
import pandas as pd
import json
import os
import random

st.set_page_config(page_title="Pandas-mop | Ola & Maciek", page_icon="✨", layout="wide")

DATA_FILE = "baza_sprzatania_50m2.json"

DEFAULT_TASKS = [
    # WEEKLY (270 min)
    {"id": "w1", "cat": "Weekly", "room": "Kuchnia", "task": "Ogarnięcie blatów i wyspy, mycie zlewu, zmywarka i naczynia ręczne", "time": 20, "default_role": "40%", "done": False},
    {"id": "w2", "cat": "Weekly", "room": "Kuchnia", "task": "Przetarcie frontów (zabudowa + wyspa), backsplashu, płyty, lodówki, piekarnika i okapu", "time": 15, "default_role": "60%", "done": False},
    {"id": "w3", "cat": "Weekly", "room": "Kuchnia", "task": "Wyniesienie śmieci i przetarcie szafki pod zlewem", "time": 10, "default_role": "40%", "done": False},
    {"id": "w4", "cat": "Weekly", "room": "Kuchnia", "task": "Wymiana ściereczek kuchennych i gąbek", "time": 3, "default_role": "40%", "done": False},
    {"id": "w5", "cat": "Weekly", "room": "Łazienka", "task": "Mycie prysznica i szyby prysznicowej (parownica + ściągaczka)", "time": 15, "default_role": "60%", "done": False},
    {"id": "w6", "cat": "Weekly", "room": "Łazienka", "task": "Czyszczenie toalety, umywalki, baterii i lustra", "time": 15, "default_role": "60%", "done": False},
    {"id": "w7", "cat": "Weekly", "room": "Łazienka", "task": "Przetarcie grzejnika i wymiana ręczników", "time": 7, "default_role": "60%", "done": False},
    {"id": "w8", "cat": "Weekly", "room": "Sypialnia", "task": "Kurze z 2 komód, szafy i ramy łóżka 160x200 + opróżnienie kosza na pranie", "time": 10, "default_role": "60%", "done": False},
    {"id": "w9", "cat": "Weekly", "room": "Sypialnia", "task": "Zmiana pościeli (łóżko 160x200, 2 kołdry, 4 poduszki)", "time": 15, "default_role": "60%", "done": False},
    {"id": "w10", "cat": "Weekly", "room": "Gabinet", "task": "Kurze z 2 biurek, regału Kallax, szafy w zabudowie i złożonego stołu Kallhall", "time": 15, "default_role": "40%", "done": False},
    {"id": "w11", "cat": "Weekly", "room": "Gabinet", "task": "Wytrzepanie i złożenie kocy do metalowego kosza", "time": 5, "default_role": "40%", "done": False},
    {"id": "w12", "cat": "Weekly", "room": "Salon", "task": "Starcie kurzy z szafki RTV, TV, szafy i stolików kawowych", "time": 10, "default_role": "40%", "done": False},
    {"id": "w13", "cat": "Weekly", "room": "Salon", "task": "Odkurzenie kanapy i fotela, ułożenie poduszek i złożenie kocy", "time": 10, "default_role": "40%", "done": False},
    {"id": "w14", "cat": "Weekly", "room": "Przedpokój", "task": "Ogarnięcie konsoli (klucze, świeczki), stojaka na buty i wieszaka na kurtki", "time": 10, "default_role": "40%", "done": False},
    {"id": "w15", "cat": "Weekly", "room": "Przedpokój", "task": "Mycie przesuwnych drzwi lustrzanych szafy (od podłogi do sufitu)", "time": 10, "default_role": "60%", "done": False},
    {"id": "w16", "cat": "Weekly", "room": "Balkon", "task": "Przetarcie szklanego stolika, 2 krzeseł i ogarnięcie wiewiórczego zakątka 🐿️", "time": 10, "default_role": "40%", "done": False},
    {"id": "w17", "cat": "Weekly", "room": "Całe 50m²", "task": "Dokładne odkurzanie całego mieszkania i balkonu", "time": 25, "default_role": "60%", "done": False},
    {"id": "w18", "cat": "Weekly", "room": "Całe 50m²", "task": "Mycie podłóg parownicą we wszystkich pomieszczeniach", "time": 25, "default_role": "60%", "done": False},
    {"id": "w19", "cat": "Weekly", "room": "Całe 50m²", "task": "Pranie w pralce kuchennej (nastawienie, rozwieszenie, poskładanie)", "time": 25, "default_role": "60%", "done": False},
    {"id": "w20", "cat": "Weekly", "room": "Całe 50m²", "task": "Podlewanie kwiatków w domu i roślin w doniczkach na balkonie", "time": 10, "default_role": "40%", "done": False},
    {"id": "w21", "cat": "Weekly", "room": "Całe 50m²", "task": "Dezynfekcja klamek i włączników światła w całym mieszkaniu", "time": 5, "default_role": "40%", "done": False},

    # MONTHLY (200 min)
    {"id": "m1", "cat": "Monthly", "room": "Kuchnia", "task": "Mycie wnętrza lodówki, przegląd zapasów i przetarcie półek", "time": 20, "default_role": "60%", "done": False},
    {"id": "m2", "cat": "Monthly", "room": "Kuchnia", "task": "Czyszczenie piekarnika i okapu (filtry + parownica)", "time": 25, "default_role": "60%", "done": False},
    {"id": "m3", "cat": "Monthly", "room": "Kuchnia", "task": "Czyszczenie pralki i zmywarki (filtry, uszczelki, szuflada)", "time": 15, "default_role": "40%", "done": False},
    {"id": "m4", "cat": "Monthly", "room": "Kuchnia", "task": "Mycie wnętrza szafki pod zlewem i pojemników na śmieci", "time": 15, "default_role": "40%", "done": False},
    {"id": "m5", "cat": "Monthly", "room": "Łazienka", "task": "Odkamienianie armatury, słuchawki prysznicowej i odpływów parownicą", "time": 15, "default_role": "60%", "done": False},
    {"id": "m6", "cat": "Monthly", "room": "Sypialnia", "task": "Odkurzanie i odświeżanie parownicą materaca 160x200, kanapy i fotela", "time": 20, "default_role": "60%", "done": False},
    {"id": "m7", "cat": "Monthly", "room": "Salon", "task": "Pranie kocy (salon, balkon, kosz w gabinecie) i poszewek poduszek", "time": 20, "default_role": "40%", "done": False},
    {"id": "m8", "cat": "Monthly", "room": "Gabinet", "task": "Rozładowanie rzeczy ze złożonego stołu Kallhall i porządek w Kallaxie", "time": 15, "default_role": "40%", "done": False},
    {"id": "m9", "cat": "Monthly", "room": "Balkon", "task": "Mycie podłogi na balkonie (mop + miednica / parownica), doniczek i barierki", "time": 25, "default_role": "60%", "done": False},
    {"id": "m10", "cat": "Monthly", "room": "Całe 50m²", "task": "Przecieranie listew przypodłogowych, górnych krawędzi drzwi i szaf", "time": 15, "default_role": "40%", "done": False},
    {"id": "m11", "cat": "Monthly", "room": "Całe 50m²", "task": "Prysznic dla kwiatków i wycieranie liści z kurzu", "time": 15, "default_role": "60%", "done": False},

    # OTHER (200 min)
    {"id": "o1", "cat": "Other", "room": "Łazienka", "task": "Mycie białych płytek ściennych od podłogi do sufitu parownicą + fugi", "time": 45, "default_role": "60%", "done": False},
    {"id": "o2", "cat": "Other", "room": "Całe 50m²", "task": "Mycie okien, ram i parapetów parownicą (salon, sypialnia, gabinet)", "time": 45, "default_role": "60%", "done": False},
    {"id": "o3", "cat": "Other", "room": "Kuchnia", "task": "Mycie wnętrza szafek w zabudowie i szafek w wyspie kuchennej", "time": 30, "default_role": "60%", "done": False},
    {"id": "o4", "cat": "Other", "room": "Balkon", "task": "Pranie zasłon zewnętrznych, 2 poduszek i koca + gruntowne mycie wiewiórczego zakątka 🐿️", "time": 30, "default_role": "40%", "done": False},
    {"id": "o5", "cat": "Other", "room": "Sypialnia", "task": "Pranie/odświeżanie 2 kołder i 4 poduszek + przegląd 2 komód i szafy", "time": 30, "default_role": "40%", "done": False},
    {"id": "o6", "cat": "Other", "room": "Przedpokój", "task": "Sezonowa rotacja kurtek i butów, porządek w szafach w zabudowie", "time": 20, "default_role": "40%", "done": False},

    # PARTY (100 min)
    {"id": "p1", "cat": "Party", "room": "Kuchnia", "task": "Opróżnienie zlewu i zmywarki na szkło gości, polerowanie blatów wyspy, frontów i backsplashu", "time": 15, "default_role": "60%", "done": False},
    {"id": "p2", "cat": "Party", "room": "Kuchnia", "task": "Wyniesienie śmieci z szafki pod zlewem (nowe worki na imprezę)", "time": 5, "default_role": "60%", "done": False},
    {"id": "p3", "cat": "Party", "room": "Łazienka", "task": "Szyba prysznicowa, lustro, umywalka i kibelek na błysk + świeży ręcznik i papier", "time": 15, "default_role": "60%", "done": False},
    {"id": "p4", "cat": "Party", "room": "Salon", "task": "Przetarcie stolików kawowych i RTV, ułożenie poduszek i kocy na kanapie i fotelu", "time": 10, "default_role": "40%", "done": False},
    {"id": "p5", "cat": "Party", "room": "Przedpokój", "task": "Miejsce na wieszaku i stojaku na buty dla gości, konsola + świeczki, przetarcie luster", "time": 10, "default_role": "40%", "done": False},
    {"id": "p6", "cat": "Party", "room": "Balkon", "task": "Schowanie mopa i miednicy, przetarcie szklanego stolika i 2 krzeseł, poduszki, koc, wiewiórczy zakątek 🐿️", "time": 10, "default_role": "40%", "done": False},
    {"id": "p7", "cat": "Party", "room": "Gabinet", "task": "Ogarnięcie 2 biurek i złożonego stołu Kallhall, koce do kosza, zaścielenie łóżka 160x200", "time": 10, "default_role": "40%", "done": False},
    {"id": "p8", "cat": "Party", "room": "Całe 50m²", "task": "Szybkie odkurzanie i odświeżenie podłóg parownicą (szczególnie strefa dzienna i łazienka)", "time": 25, "default_role": "60%", "done": False}
]

def load_state():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"person_a": "Ola", "person_b": "Maciek", "split_pct": 60, "tasks": DEFAULT_TASKS}

def save_state(state):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

state = load_state()
if "split_pct" not in state:
    state["split_pct"] = 60

tasks = state["tasks"]
df = pd.DataFrame(tasks)

st.title("✨ Pandas-mop: Centrum Dowodzenia 50 m²")

# Panel boczny
with st.sidebar:
    st.header("⚙️ Ustawienia Podziału")
    
    p_a = st.text_input("Imię Osoby A:", value=state.get("person_a", "Ola"))
    p_b = st.text_input("Imię Osoby B:", value=state.get("person_b", "Maciek"))
    
    if p_a != state["person_a"] or p_b != state["person_b"]:
        state["person_a"] = p_a
        state["person_b"] = p_b
        save_state(state)

    target_pct_a = st.slider(
        f"Cel podziału dla {p_a} (%):",
        min_value=0,
        max_value=100,
        value=int(state.get("split_pct", 60)),
        step=5
    )
    
    if target_pct_a != state["split_pct"]:
        state["split_pct"] = target_pct_a
        save_state(state)

    target_pct_b = 100 - target_pct_a
    st.info(f"Aktualny cel: **{p_a} ({target_pct_a}%)** / **{p_b} ({target_pct_b}%)**")

    st.divider()
    st.header("🔍 Filtry")
    selected_owner = st.selectbox("Pokaż zadania dla:", ["Wszyscy", p_a, p_b])
    rooms = ["Wszystkie"] + sorted(df["room"].unique().tolist())
    selected_room = st.selectbox("Pomieszczenie:", rooms)
    
    st.divider()
    st.header("🎲 Algorytmy")
    if st.button("🔀 Wylosuj podział pod wybrane %"):
        for cat in ["Weekly", "Monthly", "Other", "Party"]:
            cat_tasks = [t for t in tasks if t["cat"] == cat]
            total = sum(t["time"] for t in cat_tasks)
            target_time_a = total * (target_pct_a / 100.0)
            
            best_diff = 9999
            best_assign = []
            for _ in range(400):
                random.shuffle(cat_tasks)
                curr_sum = 0
                assign = []
                for t in cat_tasks:
                    if curr_sum + t["time"] <= target_time_a + 4:
                        curr_sum += t["time"]
                        assign.append((t["id"], p_a))
                    else:
                        assign.append((t["id"], p_b))
                if abs(curr_sum - target_time_a) < best_diff:
                    best_diff = abs(curr_sum - target_time_a)
                    best_assign = assign
            
            assign_dict = dict(best_assign)
            for t in tasks:
                if t["id"] in assign_dict:
                    t["owner"] = assign_dict[t["id"]]
        save_state(state)
        st.rerun()

    if st.button("🔄 Odznacz wszystkie zadania"):
        for t in tasks:
            t["done"] = False
        save_state(state)
        st.rerun()

tabs = st.tabs(["📅 Cotygodniowe (Weekly)", "🗓️ Comiesięczne (Monthly)", "🧼 Sezonowe (Other)", "🎉 Przed Imprezą"])
categories = ["Weekly", "Monthly", "Other", "Party"]

for tab, cat in zip(tabs, categories):
    with tab:
        cat_df = df[df["cat"] == cat].copy()
        
        total_time = int(cat_df["time"].sum())
        time_a = int(cat_df[cat_df["owner"] == p_a]["time"].sum()) if "owner" in cat_df.columns else 0
        time_b = int(cat_df[cat_df["owner"] == p_b]["time"].sum()) if "owner" in cat_df.columns else 0
        done_time = int(cat_df[cat_df["done"] == True]["time"].sum())
        
        actual_pct_a = round((time_a / total_time) * 100) if total_time else 0
        actual_pct_b = 100 - actual_pct_a if total_time else 0
        pct_done = round((done_time / total_time) * 100) if total_time else 0

        col1, col2, col3 = st.columns(3)
        col1.metric(f"👤 {p_a} (Cel: {target_pct_a}%)", f"{time_a} min ({actual_pct_a}%)", f"{actual_pct_a - target_pct_a}% od celu")
        col2.metric(f"👤 {p_b} (Cel: {target_pct_b}%)", f"{time_b} min ({actual_pct_b}%)", f"{actual_pct_b - target_pct_b}% od celu")
        col3.metric("✅ Postęp wykonania", f"{pct_done}% ({done_time}/{total_time} min)")
        
        st.progress(pct_done / 100)
        
        if pct_done == 100 and total_time > 0:
            st.success("🎉 Wszystko w tej kategorii lśni czystością!")

        view_df = cat_df.copy()
        if selected_owner != "Wszyscy":
            view_df = view_df[view_df["owner"] == selected_owner]
        if selected_room != "Wszystkie":
            view_df = view_df[view_df["room"] == selected_room]

        edited_df = st.data_editor(
            view_df[["id", "done", "room", "task", "time", "owner"]],
            column_config={
                "id": None,
                "done": st.column_config.CheckboxColumn("Zrobione?", default=False),
                "room": st.column_config.TextColumn("Strefa", disabled=True),
                "task": st.column_config.TextColumn("Zadanie", width="large"),
                "time": st.column_config.NumberColumn("Czas (min)", min_value=1, max_value=180, step=1),
                "owner": st.column_config.SelectboxColumn("Kto robi?", options=[p_a, p_b], required=True),
            },
            hide_index=True,
            use_container_width=True,
            key=f"editor_{cat}"
        )

        if not edited_df.equals(view_df[["id", "done", "room", "task", "time", "owner"]]):
            updates = edited_df.set_index("id").to_dict(orient="index")
            for t in tasks:
                if t["id"] in updates:
                    t["done"] = bool(updates[t["id"]]["done"])
                    t["owner"] = updates[t["id"]]["owner"]
                    t["time"] = int(updates[t["id"]]["time"])
                    t["task"] = updates[t["id"]]["task"]
            
            cat_tasks_now = [t for t in tasks if t["cat"] == cat]
            if all(t["done"] for t in cat_tasks_now):
                st.balloons()
                
            save_state(state)
            st.rerun()
