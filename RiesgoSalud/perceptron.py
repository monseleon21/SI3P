#Estas son las importaciones para poder crear cajas de texto interactivas
import tkinter as tk
from tkinter import messagebox
import numpy as np

#Aqui esta la configuracion del perceptron y su formula
PESOS = np.array([
    -0.4, # Frutas y verduras (Si se come mas frutas = menos riesgo)
    -0.6, #Ejercicio (Mas ejercicio = menos riesgo)
    1.2, #Fumador (Si fuma  = más riesgo)
    0.05, # Edad (Mayor edad = más riesgo, pero muy poco)
    1.0, #Hereditarias (si tiene = mas riesgo)
    0.9, #Frcaturas (si tiene = muy poco peso de riesgo)
    1.5]) #Cronicas (si tiene = peso un mas alto)
BIAS = -4.0

# Variables 
nombre_usuario = ""
edad_usuario = 0
historial_eval = []  #Historial de usuarios


def funcion_activacion(valor):
    return 1 if valor >= 0 else 0

#  np.dot multiplica todos los datos del usuario por sus pesos y luego le suma el bias
def evaluar_riesgo(datos):
    suma = np.dot(datos, PESOS) + BIAS
    salida = funcion_activacion(suma)
    return salida, suma

#interfaz
def mostrar_entrada_nombre():
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.geometry("400x250")
    ventana.configure(bg="#e8f0fe")
    tk.Label(ventana, text="🩺 Evaluador de Riesgo Médico", font=("Arial", 14, "bold"), bg="#e8f0fe").pack(pady=15)
    tk.Label(ventana, text="Tu nombre:", bg="#e8f0fe").pack()
    entry_nombre_local = tk.Entry(ventana)
    entry_nombre_local.pack()
    tk.Label(ventana, text="Tu edad:", bg="#e8f0fe").pack()
    entry_edad_local = tk.Entry(ventana)
    entry_edad_local.pack()

    def continuar():
        global nombre_usuario, edad_usuario
        try:
            nombre_usuario = entry_nombre_local.get()
            edad_usuario = int(entry_edad_local.get())
            mostrar_formulario()
        except:
            messagebox.showerror("Error", "Ingresa un nombre y una edad válida.")
    tk.Button(ventana, text="Continuar", bg="#4CAF50", fg="white", command=continuar).pack(pady=15)

#interfaz Formulario 
def mostrar_formulario():
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.geometry("450x600")
    ventana.configure(bg="#e8f0fe")
    tk.Label(ventana, text=f"Formulario de Salud - {nombre_usuario} ({edad_usuario} años)", font=("Arial", 10, "italic"), bg="#e8f0fe").pack(pady=10)
    entradas = {}

    def agregar_campo(titulo, ayuda=None):
        tk.Label(ventana, text=titulo, anchor="w", bg="#e8f0fe").pack(fill="x", padx=20)
        if ayuda:
            tk.Label(ventana, text=ayuda, font=("Arial", 8), fg="gray", bg="#e8f0fe").pack()
        entrada = tk.Entry(ventana)
        entrada.pack(fill="x", padx=20)
        return entrada

    entradas['frutas'] = agregar_campo("Porciones diarias de frutas/verduras:")
    entradas['ejercicio'] = agregar_campo("Horas de ejercicio semanales:")
    entradas['fuma'] = agregar_campo("¿Fuma? (1 = Sí, 0 = No):")
    entradas['hereditario'] = agregar_campo("¿Enfermedades hereditarias? (1 = Sí, 0 = No):", "Ej: Diabetes, hipertensión en familia")
    entradas['fracturas'] = agregar_campo("¿Fracturas importantes? (1 = Sí, 0 = No):", "Ej: pierna rota, columna, brazo con yeso")
    entradas['cronico'] = agregar_campo("¿Enfermedades crónicas? (1 = Sí, 0 = No):", "Ej: Asma, epilepsia, diabetes, hipertensión")


#esta es la part de la automatización 
#se pregunta al usuario si ha tenido alguno de los 3 factores de riesgo de salud en su historiaL medico
# cada respuesta solo acepta un si = 2 o no=0
#los calculos se incluyen automaticamente en la suma del riesgo 
    def evaluar():
        try:
            frutas = int(entradas['frutas'].get())
            ejercicio = int(entradas['ejercicio'].get())
            fuma = int(entradas['fuma'].get())
            hereditario = int(entradas['hereditario'].get())
            fracturas = int(entradas['fracturas'].get())
            cronico = int(entradas['cronico'].get())
            datos = np.array([frutas, ejercicio, fuma, edad_usuario, hereditario, fracturas, cronico]) # aqui es donde se estan inlcuyendo 
            resultado, _ = evaluar_riesgo(datos)

            causas = []
            if frutas < 3: causas.append("pocas frutas")
            if ejercicio < 2: causas.append("poco ejercicio")
            if fuma == 1: causas.append("fuma")
            if edad_usuario > 45: causas.append("edad avanzada")
            if hereditario == 1: causas.append("enfermedades hereditarias")
            if fracturas == 1: causas.append("fracturas previas")
            if cronico == 1: causas.append("enfermedades crónicas")

            mensaje = f"🩺 Resultado para {nombre_usuario}:\n\n"
            nivel = "ALTO" if resultado == 1 else "BAJO"
            mensaje += " Riesgo ALTO. Se recomienda tener seguro médico.\n" if resultado == 1 else "🟢 Riesgo BAJO. No es obligatorio tener seguro médico.\n"
            if causas:
                mensaje += "\nFactores considerados: " + ", ".join(causas) + "."

            # historial aqui se guad¿rda todo con las varibles de nombre, edad ,niveles y causa 
            historial_eval.append({
                "nombre": nombre_usuario,
                "edad": edad_usuario,
                "riesgo": nivel,
                "factores": causas})
            messagebox.showinfo("Resultado del Análisis", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Verifica que todos los campos estén llenos y correctos.\n{e}")

    # Botones Evaluar + Historial
    boton_frame = tk.Frame(ventana, bg="#e8f0fe")
    boton_frame.pack(pady=20)
    tk.Button(boton_frame, text="Evaluar Riesgo", command=evaluar, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Button(boton_frame, text="Historial", command=mostrar_historial, bg="#607D8B", fg="white", font=("Arial", 10)).pack(side="left", padx=10)

# Historial de evaluaciones
def mostrar_historial():
    if not historial_eval:
        messagebox.showinfo("Historial", "No hay personas evaluadas aún.")
        return

    historial_texto = ""
    for idx, persona in enumerate(historial_eval, 1):
        historial_texto += f"{idx}. {persona['nombre']} ({persona['edad']} años)\n"
        historial_texto += f"   Riesgo: {persona['riesgo']}\n"
        if persona['factores']:
            historial_texto += f"   Factores: {', '.join(persona['factores'])}\n"
        historial_texto += "\n"
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de Evaluaciones")
    ventana_historial.geometry("400x400")
    ventana_historial.config(bg="#fff")
    text_widget = tk.Text(ventana_historial, wrap="word", font=("Arial", 10))
    text_widget.insert("1.0", historial_texto)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)


#inicio de la ventana  
ventana = tk.Tk()
ventana.title("Evaluador de Riesgo Médico")
ventana.configure(bg="#e8f0fe")

mostrar_entrada_nombre()
ventana.mainloop()
