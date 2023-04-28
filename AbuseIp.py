import tkinter as tk
import requests

API_KEY = 'Put your API'
ABUSEIPDB_URL = 'https://api.abuseipdb.com/api/v2/check'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.configure(background='#2b2b2b')
        self.master.title('Análisis de IPs')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.ips_label = tk.Label(self, text='Direcciones IP (separadas por comas):', fg='#c8c8c8', bg='#2b2b2b', font=('Helvetica', 12))
        self.ips_label.pack(side='top', pady=10)

        self.ips_entry = tk.Entry(self, width=50, bg='white', fg='black', font=('Helvetica', 12))
        self.ips_entry.pack(side='top')

        self.analyze_button = tk.Button(self, text='Analizar', command=self.analyze_ips, bg='#5ca36a', fg='#ffffff', font=('Helvetica', 12, 'bold'))
        self.analyze_button.pack(side='top', pady=10)

        self.result_label = tk.Label(self, text='Resultados:', fg='#c8c8c8', bg='#2b2b2b', font=('Helvetica', 12))
        self.result_label.pack(side='top', pady=10)

        self.result_text = tk.Text(self, height=20, width=50, bg='#444444', fg='#c8c8c8', font=('Helvetica', 12))
        self.result_text.pack(side='top')
        self.result_text.config(font=("Consolas", 11))
        
    def analyze_ips(self):
        self.result_text.delete('1.0', tk.END)

        ips = self.ips_entry.get().strip()
        if not ips:
            self.result_text.insert(tk.END, 'Debe ingresar al menos una dirección IP')
            return

        ips_list = ips.split(',')
        for ip in ips_list:
            ip = ip.strip()
            if not ip:
                continue

            try:
                response = requests.get(ABUSEIPDB_URL, headers={'Key': API_KEY}, params={'ipAddress': ip}, verify=False) # change to TRUE IF YOU WANT SSL ON
                response.raise_for_status()
                data = response.json()

                self.result_text.insert(tk.END, f'IP: {data["data"]["ipAddress"]}\n', 'bold')
                self.result_text.insert(tk.END, f'Total de informes: {data["data"]["totalReports"]}\n')
                self.result_text.insert(tk.END, f'Confianza: {data["data"]["abuseConfidenceScore"]}\n')
                self.result_text.insert(tk.END, f'Último informe: {data["data"]["lastReportedAt"]}\n')
                comments = data["data"].get('comments', 'No hay comentarios disponibles')
                self.result_text.insert(tk.END, f'Comentarios: {comments}\n')
                isp = data["data"].get('isp', 'No se encontró información del ISP')
                self.result_text.insert(tk.END, f'ISP: {isp}\n')
                city = data["data"].get('cityName', 'No se encontró información de la ciudad')
                self.result_text.insert(tk.END, f'Ciudad: {city}\n')
                country = data["data"].get('countryName', 'No se encontró información del país')
                self.result_text.insert(tk.END, f'País: {country}\n')
            except requests.exceptions.HTTPError as e:
                self.result_text.insert(tk.END, f'Error al consultar la IP {ip}: {e}\n')
            except requests.exceptions.RequestException as e:
                self.result_text.insert(tk.END, f'Error al consultar la IP {ip}: {e}\n')

# Ejecutar ventana
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
