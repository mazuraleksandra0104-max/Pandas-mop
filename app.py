import streamlit as st
import pandas as pd
import json
import os
import random

st.set_page_config(page_title="Pandas-mop | Ola & Maciek", page_icon="✨", layout="wide")

DATA_FILE = "baza_v2.json"

DEFAULT_TASKS = [
    # DAILY (Codzienne)
    {"id": "d1", "cat": "Daily", "room": "Kuchnia", "task": "Ogarnięcie blatów, wyspy i zlewu po całym dniu", "time": 10, "default_role": "40%", "done": False},
    {"id": "d2", "cat": "Daily", "room": "Kuchnia", "task": "Wrzucenie naczyń do zmywarki / włączenie zmywarki", "time": 5, "default_role": "40%", "done": False},
    {"id": "d3", "cat": "Daily", "room": "Salon", "task": "Złożenie kocy, poprawienie poduszek na kanapie i fotelu", "time": 5, "default_role": "40%", "done": False},
    {"id": "d4", "cat": "Daily", "room": "Sypialnia", "task": "Narzucenie kołder / lekkie przewietrzenie wkładów", "time": 5, "default_role": "60%", "done": False},
    {"id": "d5", "cat": "Daily", "room": "Przedpokój", "task": "Odstawienie butów na stojak, odwieszenie kurtek", "time": 5, "default_role": "40%", "done": False},

    # WEEKLY (Cotygodniowe)
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

    # MONTHLY (Comiesięczne)
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

    # OTHER (Sezonowe)
    {"id": "o1", "cat": "Other", "room": "Łazienka", "task": "Mycie białych płytek ściennych od podłogi do sufitu parownicą + fugi", "time": 45, "default_role": "60%", "done": False},
    {"id": "o2", "cat": "Other", "room": "Całe 50m²", "task": "Mycie okien, ram i parapetów parownicą (salon, sypialnia, gabinet)", "time": 45, "default_role": "60%", "done": False},
    {"id": "o3", "cat": "Other", "room": "Kuchnia", "task": "Mycie wnętrza szafek w zabudowie i szafek w wyspie kuchennej", "time": 30, "default_role": "60%", "done": False},
    {"id": "o4", "cat": "Other", "room": "Balkon", "task": "Pranie zasłon zewnętrznych, 2 poduszek i koca + gruntowne mycie wiewiórczego zakątka 🐿️", "time": 30, "default_role": "40%", "done": False},
    {"id": "o5", "cat": "Other", "room": "Sypialnia", "task": "Pranie/odświeżanie 2 kołder i 4 poduszek + przegląd 2 komód i szafy", "time": 30, "default_role": "40%", "done": False},
    {"id": "o6", "cat": "Other", "room": "Przedpokój", "task": "Sezonowa rotacja kurtek i butów, porządek w szafach w zabudowie", "time": 20, "default_role": "40%", "done": False},

    # PARTY (Przed imprezą)
    {"id": "p1", "cat": "Party", "room": "Kuchnia", "task": "Opróżnienie zlewu i zmywarki na szkło gości, polerowanie blatów wyspy, frontów i backsplashu", "time": 15, "default_role": "60%", "done": False},
    {"id": "p2", "cat": "Party", "room": "Kuchnia", "task": "Wyniesienie śmieci z szafki pod zlewem (nowe worki na imprezę)", "time": 5, "default_role": "60%", "done": False},
    {"id": "p3", "cat": "Party", "room": "Łazienka", "task": "Szyba prysznicowa, lustro, umywalka i kibelek na błysk + świeży ręcznik i papier", "time": 15, "default_role": "60%", "done": False},
    {"id": "p4", "cat": "Party", "room": "Salon", "task": "Przetarcie stolików kawowych i RTV, ułożenie poduszek i kocy na kanapie i fotelu", "time": 10, "default_role": "40%", "done": False},
    {"id": "p5", "cat": "Party", "room": "Przedpokój", "task": "Miejsce na wieszaku i stojaku na buty dla gości, konsola + świeczki, przetarcie luster", "time": 10, "default_role": "40%", "done": False},
    {"id": "p6", "cat": "Party", "room": "Balkon", "task": "Schowanie mopa i miednicy, przetarcie szklanego stolika i 2 krzeseł, poduszki, koc, wiewiórczy zakątek 🐿️", "time": 10, "default_role": "40%", "done": False},
    {"id": "p7", "cat": "Party", "room": "Gabinet", "task": "Ogarnięcie 2 biurek i złożonego stołu Kallhall, koce do kosza, zaścielenie łóżka 160x200", "time": 10, "default_role": "40%", "done": False},
    {"id": "p8", "cat": "Party", "room": "Całe 50m²", "task": "Szybkie odkurzanie i odświeżenie podłóg parownicą (szczególnie strefa dzienna i łazienka)", "time": 25, "default_role": "60%", "done": False},

    # PROJECTS (Zadania specjalne / Projekty)
    {"id": "pr1", "cat": "Projects", "room": "Sypialnia", "task": "Gruntowne sprzątanie szafy z ubraniami (selekcja, poukładanie)", "time": 90, "default_role": "60%", "done": False},
    {"id": "pr2", "cat": "Projects", "room": "Gabinet", "task": "Organizacja regału Kallax i dokumentów w szafie", "time": 60, "default_role": "40%", "done": False},
    {"id": "pr3", "cat": "Projects", "room": "Kuchnia", "task": "Mycie wszystkich szafek w zabudowie od środka", "time": 120, "default_role": "60%", "done": False}
]

def load_state():
    p_a = "Ola"
    p_b = "Maciek"
    tasks = DEFAULT_TASKS.copy()
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                p_a = loaded.get("person_a", "Ola")
                p_b = loaded.get("person_b", "Maciek")
                if "tasks" in loaded:
                    loaded_tasks = loaded["tasks"]
                    loaded_map = {t["id"]: t for t in loaded_tasks}
                    for dt in tasks:
                        if dt["id"] not in loaded_map:
                            dt["owner"] = p_a if dt.get("default_role") == "60%" else p_b
                            loaded_tasks.append(dt)
                    tasks = loaded_tasks
        except:
            pass

    for t in tasks:
        if "owner" not in t:
            t["owner"] = p_a if t.get("default_role") == "60%" else p_b
        if "done" not in t:
            t["done"] = False

    return {
        "person_a": p_a,
        "person_b": p_b,
        "split_pct": 60,
        "tasks": tasks
    }

def save_state(state):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

state = load_state()
if "split_pct" not in state:
    state["split_pct"] = 60

p_a = state["person_a"]
p_b = state["person_b"]
tasks = state["tasks"]

st.title("✨ Pandas-mop: Centrum Dowodzenia ✨")

with st.sidebar:
    st.header("⚙️ Ustawienia Podziału")
    
    new_p_a = st.text_input("Imię Osoby A:", value=p_a)
    new_p_b = st.text_input("Imię Osoby B:", value=p_b)
    
    if new_p_a != p_a or new_p_b != p_b:
        state["person_a"] = new_p_a
        state["person_b"] = new_p_b
        for t in tasks:
            if t["owner"] == p_a:
                t["owner"] = new_p_a
            elif t["owner"] == p_b:
                t["owner"] = new_p_b
        save_state(state)
        st.rerun()

    target_pct_a = st.slider(
        f"Cel podziału dla {new_p_a} (%):",
        min_value=0,
        max_value=100,
        value=int(state.get("split_pct", 60)),
        step=5
    )
    
    if target_pct_a != state["split_pct"]:
        state["split_pct"] = target_pct_a
        save_state(state)

    target_pct_b = 100 - target_pct_a
    st.info(f"Aktualny cel: **{new_p_a} ({target_pct_a}%)** / **{new_p_b} ({target_pct_b}%)**")

    st.divider()
    st.header("🔍 Filtry")
    selected_owner = st.selectbox("Pokaż zadania dla:", ["Wszyscy", new_p_a, new_p_b])
    
    temp_df = pd.DataFrame(tasks)
    rooms = ["Wszystkie"] + sorted(temp_df["room"].unique().tolist()) if not temp_df.empty else ["Wszystkie"]
    selected_room = st.selectbox("Pomieszczenie:", rooms)
    
    st.divider()
    st.header("🎲 Algorytmy")
    if st.button("🔀 Wylosuj podział pod wybrane %"):
        for cat in ["Daily", "Weekly", "Monthly", "Other", "Party", "Projects"]:
            cat_tasks = [t for t in tasks if t["cat"] == cat]
            if not cat
