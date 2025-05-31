import sys
import os
import pandas as pd
import random

try:
    import tkinter as tk
    from tkinter import simpledialog
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    print("Este script requiere un entorno gráfico con tkinter y PIL instalados.")
    sys.exit(1)

# Verifica que el archivo exista
csv_file = "Dataset/colombian_coffee_dataset.csv"
if not os.path.exists(csv_file):
    print(f"No se encuentra el archivo '{csv_file}'. Asegúrate de que esté en el mismo directorio.")
    sys.exit(1)

df = pd.read_csv(csv_file)

# Iniciar ventana
root = tk.Tk()
root.withdraw()

# Preguntar el nombre
user_name = simpledialog.askstring("Bienvenido", "¿Cómo te llamas?")
if not user_name:
    user_name = "amigo"

root.deiconify()
root.title("Chatbot Agro_conecta")
root.geometry("800x600")

# Fondo
try:
    bg_image = Image.open("paisaje_cafetero.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image.resize((800, 600)))
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    print("Imagen de fondo no encontrada.")

# Imagen recolectora
try:
    collector_img = Image.open("recolectora_sonriendo.png")
    collector_photo = ImageTk.PhotoImage(collector_img.resize((150, 200)))
    collector_label = tk.Label(root, image=collector_photo, bg='white')
    collector_label.place(x=620, y=10)
except FileNotFoundError:
    print("Imagen recolectora no encontrada.")

# Área de chat
chat_frame = tk.Frame(root, bg='white', bd=2)
chat_frame.place(x=20, y=20, width=580, height=460)
chat_log = tk.Text(chat_frame, wrap='word', bg='white', fg='black')
chat_log.pack(expand=True, fill='both')
chat_log.insert(tk.END, f"Recolectora: ¡Hola {user_name.capitalize()}! Soy Aracelly 😊. Pregúntame sobre nuestras variedades de café, precios, calidad, bonos de carbono, año de cosecha.\n")

# Entrada de texto
user_input = tk.Entry(root, width=80)
user_input.place(x=20, y=500)

# Responder
def respond():
    question = user_input.get().lower()
    chat_log.insert(tk.END, f"\n{user_name.capitalize()}: {question}\n")

    response = "Lo siento, no entendí tu pregunta. ¿Quieres saber sobre variedades, precios, calidad, año de cosecha o productores?"

    # Sinónimos
    variedad_keys = ["variedad", "tipo", "clase"]
    precio_keys = ["precio", "cuánto", "cuesta", "vale", "valor", "tarifa"]
    calidad_keys = ["calidad", "score", "puntaje", "ranking"]
    año_keys = ["año", "cosecha", "producción"]
    productor_keys = ["productor", "campesino", "cultivador"]

    if any(word in question for word in variedad_keys):
        variedades = df['coffee_variety'].dropna().unique()
        response = f"Nuestras variedades incluyen: {', '.join(sorted(variedades))}."

    elif any(word in question for word in precio_keys):
        encontrada = False
        for variedad in df['coffee_variety'].dropna().unique():
            if variedad.lower() in question:
                encontrada = True
                precios = df[df['coffee_variety'].str.lower() == variedad.lower()]['price']
                precio_min = round(precios.min(), 2)
                precio_max = round(precios.max(), 2)
                response = f"El café de variedad {variedad} cuesta entre ${precio_min} y ${precio_max} USD por libra."
                break
        if not encontrada:
            response = "Por favor dime qué variedad de café te interesa para decirte el precio."

    elif any(word in question for word in calidad_keys):
        ranking = df['ranking'].dropna()
        promedio = round(ranking.mean(), 2)
        response = f"La calidad promedio de nuestros cafés es {promedio} puntos sobre 100."

    elif any(word in question for word in año_keys):
        años = sorted(df['year'].dropna().unique())
        response = f"Tenemos cafés de las siguientes cosechas: {', '.join(map(str, años))}."

    elif any(word in question for word in productor_keys):
        name = df.sample(1).iloc[0]['name']
        response = f"Uno de nuestros productores es {name}, ¡cultiva con mucho cariño y dedicación!"

    elif "bono" in question or "carbono" in question:
        # Este dato no está, se simula
        bono = random.uniform(0.5, 2.5)
        response = f"Nuestros cafés pueden generar en promedio {bono:.2f} bonos de carbono por lote certificado."

    elif "hola" in question or "buenos días" in question or "saludo" in question:
        response = f"¡Hola {user_name.capitalize()}! ¿Cómo estás? 😊 ¿Sobre qué café quieres saber hoy?"

    chat_log.insert(tk.END, f"Recolectora: {response}\n")
    user_input.delete(0, tk.END)

# Botón enviar
# Botón Enviar con estilo moderno
send_button = tk.Button(
    root,
    text="✉️ Enviar",
    command=respond,
    bg="#4CAF50",       # Verde profesional
    fg="white",         # Texto blanco
    font=("Helvetica", 11, "bold"),
    activebackground="#20a025",  # Color al hacer clic
    activeforeground="white",
    relief="raised",
    bd=3,
    padx=5,
    pady=5,
    cursor="hand2"
)
send_button.place(x=550, y=490)
user_input.bind("<Return>", lambda event: respond())

# Entrada de texto
user_input = tk.Entry(root, width=80)
user_input.place(x=20, y=500)

# Enviar al presionar Enter
user_input.bind("<Return>", lambda event: respond())


# Función para insertar texto en el campo de entrada
def sugerencia(texto):
    user_input.delete(0, tk.END)
    user_input.insert(0, texto)

# Función para insertar texto en el campo de entrada
def sugerencia(texto):
    user_input.delete(0, tk.END)
    user_input.insert(0, texto)

# Estilo común para los botones
def crear_boton_sugerencia(frame, texto, pregunta, color, columna):
    boton = tk.Button(
        frame, text=texto, command=lambda: sugerencia(pregunta),
        bg=color, fg='black', font=('Helvetica', 10, 'bold'),
        relief='raised', bd=2, padx=10, pady=5, cursor='hand2'
    )
    boton.grid(row=0, column=columna, padx=5, pady=5)
    boton.configure(highlightbackground='gray', highlightthickness=1)

# Frame de sugerencias
sugerencias_frame = tk.Frame(root, bg='white')
sugerencias_frame.place(x=20, y=540)

# Crear botones personalizados
crear_boton_sugerencia(sugerencias_frame, "🌱 Variedades", "¿Qué variedades de café tienen?", "#e0f7fa", 0)
crear_boton_sugerencia(sugerencias_frame, "💰 Precios", "¿Cuánto cuesta el café?", "#fff9c4", 1)
crear_boton_sugerencia(sugerencias_frame, "📈 Calidad", "¿Cuál es la calidad del café?", "#c8e6c9", 2)
crear_boton_sugerencia(sugerencias_frame, "📅 Año cosecha", "¿De qué año es el café?", "#f8bbd0", 3)
crear_boton_sugerencia(sugerencias_frame, "🌍 Bonos carbono", "¿Qué bonos de carbono generan los cafés?", "#d1c4e9", 4)

# Ejecutar interfaz
tk.mainloop()