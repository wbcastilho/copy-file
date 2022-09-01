import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from tkinter import filedialog
import shutil
from widgets.MaskedInt import MaskedInt
import datetime


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.photoimages = []
        self.start = False
        self.intime = False

        self.source_file = ttk.StringVar()
        self.destination_path = ttk.StringVar()
        self.interval = ttk.StringVar()
        self.hour = ttk.StringVar()
        self.minute = ttk.StringVar()
        self.second = ttk.StringVar()
        self.name = ttk.StringVar()
        self.afterid = ttk.StringVar()

        self.hour_values = []
        self.minute_values = []
        self.second_values = []

        self.entry_interval = None
        self.combobox_hour = None
        self.combobox_minute = None
        self.combobox_second = None
        self.entry_name = None
        self.button_action = None
        self.button_source_file = None
        self.button_destination_path = None

        masked_int = MaskedInt()
        self.digit_func = self.register(masked_int.mask_number)

        self.init_combobox()
        self.associate_icons()
        self.create_buttonbar()
        self.create_path_frame()

    def associate_icons(self):
        image_files = {
            'play': 'icons8-reproduzir-24.png',
            'stop': 'icons8-parar-24.png',
            'settings-light': 'icons8-configuracoes-24.png',
            'refresh': 'icons8-actualizar-24.png'
        }

        imgpath = Path(__file__).parent / '../assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

    def init_combobox(self):
        for i in range(0, 60):
            number = "0" + str(i) if i < 10 else str(i)
            if i <= 23:
                self.hour_values.append(number)
            self.minute_values.append(number)
            self.second_values.append(number)

    def create_buttonbar(self):
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        self.button_action = ttk.Button(
            master=buttonbar, text='Iniciar',
            image='play',
            compound=LEFT,
            command=self.on_action
        )
        self.button_action.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        '''btn = ttk.Button(
            master=buttonbar,
            text='Configurações',
            image='settings-light',
            compound=LEFT
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)'''

    def create_path_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=20, pady=15)

        label = ttk.Label(frame, text="Origem")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E)

        entry = ttk.Entry(frame, width=50, state="disabled", textvariable=self.source_file)
        entry.grid(row=0, column=1, padx=2, sticky=ttk.W)

        self.button_source_file = ttk.Button(frame, text="Selecionar Arquivo", width=18, bootstyle=(INFO, OUTLINE),
                                             command=self.on_browse_file)
        self.button_source_file.grid(row=0, column=2, padx=2)

        label = ttk.Label(frame, text="Destino")
        label.grid(row=1, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        entry = ttk.Entry(frame, width=50, state="disabled", textvariable=self.destination_path)
        entry.grid(row=1, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

        self.button_destination_path = ttk.Button(frame, text="Selecionar Pasta", width=18, bootstyle=(INFO, OUTLINE),
                                                  command=self.on_browse_folder)
        self.button_destination_path.grid(row=1, column=2, padx=2, pady=(20, 0), sticky=ttk.W)

        label = ttk.Label(frame, text="Nome Arquivo")
        label.grid(row=2, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        self.entry_name = ttk.Entry(frame, width=50, textvariable=self.name)
        self.entry_name.grid(row=2, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

        label = ttk.Label(frame, text="Intervalo")
        label.grid(row=3, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        self.entry_interval = ttk.Entry(frame, width=10, justify="center", textvariable=self.interval, validate="key",
                                        validatecommand=(self.digit_func, '%S', '%P', '%d'))
        self.entry_interval.grid(row=3, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

        label = ttk.Label(frame, text="Horário Agendamento")
        label.grid(row=4, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        frame2 = ttk.Frame(frame)
        frame2.grid(row=4, column=1, pady=(20, 0), sticky=ttk.W)

        self.combobox_hour = ttk.Combobox(frame2, width=10, justify="center", textvariable=self.hour,
                                          values=self.hour_values)
        self.combobox_hour.grid(row=0, column=0, padx=2, sticky=ttk.W)

        label = ttk.Label(frame2, text=":", font='Arial 10 bold',)
        label.grid(row=0, column=1, padx=1, pady=0)

        self.combobox_minute = ttk.Combobox(frame2, width=10, justify="center", textvariable=self.minute,
                                            values=self.minute_values)
        self.combobox_minute.grid(row=0, column=2, padx=2, sticky=ttk.W)

        label = ttk.Label(frame2, text=":", font='Arial 10 bold',)
        label.grid(row=0, column=3, padx=1, pady=0)

        self.combobox_second = ttk.Combobox(frame2, width=10, justify="center", textvariable=self.second,
                                            values=self.second_values)
        self.combobox_second.grid(row=0, column=4, padx=2, sticky=ttk.W)

    def on_browse_folder(self):
        path = filedialog.askdirectory(initialdir=r'c:\\', title="Selecionar Pasta")
        if path:
            self.destination_path.set(path)

    def on_browse_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title='Selecionar Arquivo', initialdir='c:/', filetypes=filetypes)
        if filename:
            self.source_file.set(filename)

    def on_action(self):
        if not self.start:
            if self.validate():
                self.change_button_action_state(False)
                self.change_form_state(False)
                self.start = True
                self.after(0, self.loop)
        else:
            self.change_button_action_state(True)
            self.change_form_state(True)
            self.start = False
            self.after_cancel(self.afterid.get())

    def loop(self):
        try:
            current_date = datetime.datetime.now()
            if self.hour.get() == current_date.strftime("%H") and self.minute.get() == current_date.strftime("%M"):
                if not self.intime:
                    self.intime = True
                    file = f"{self.destination_path.get()}/{self.name.get()}{current_date.strftime('%d_%m_%y')}.txt"
                    print(file)
                    shutil.copy2(self.source_file.get(), file)
            else:
                self.intime = False
        except Exception as err:
            print(err)
            self.intime = False
            messagebox.showerror(title="Erro", message="Erro ao copiar arquivo.")
        finally:
            time = int(self.interval.get()) * 1000
            self.afterid.set(self.after(time, self.loop))

    def validate(self):
        def validate_source_file(cls):
            if cls.source_file.get() == "" or cls.source_file.get() is None:
                messagebox.showwarning(title="Atenção", message="Selecione o arquivo de origem.")
                return False
            return True

        def validate_destination_path(cls):
            if cls.destination_path.get() == "" or cls.destination_path.get() is None:
                messagebox.showwarning(title="Atenção", message="Selecione o diretório de destino.")
                return False
            return True

        def validate_interval(cls):
            if cls.interval.get() == "" or cls.interval.get() is None:
                messagebox.showwarning(title="Atenção", message="O campo intervalo deve ser preenchido.")
                return False
            elif int(cls.interval.get()) <= 0:
                messagebox.showwarning(title="Atenção", message="O tempo de sincronismo deve ser maior ou igual a 0.")
                return False
            return True

        def validate_combobox_hour(cls):
            if cls.hour.get() == "" or cls.hour.get() is None:
                messagebox.showwarning(title="Atenção", message="O campo hora dever ser selecionado.")
                return False
            elif not cls.hour.get().isdigit():
                messagebox.showwarning(title="Atenção", message="Hora inválida")
                return False
            elif int(cls.hour.get()) > 23 or int(cls.hour.get()) < 0:
                messagebox.showwarning(title="Atenção", message="Hora inválida")
                return False
            return True

        def validate_combobox_minute(cls):
            if cls.minute.get() == "" or cls.minute.get() is None:
                messagebox.showwarning(title="Atenção", message="O campo minuto dever ser selecionado.")
                return False
            elif not cls.minute.get().isdigit():
                messagebox.showwarning(title="Atenção", message="Minuto inválida")
                return False
            elif int(cls.minute.get()) > 59 or int(cls.minute.get()) < 0:
                messagebox.showwarning(title="Atenção", message="Minuto inválida")
                return False
            return True

        def validate_combobox_second(cls):
            if cls.second.get() == "" or cls.second.get() is None:
                messagebox.showwarning(title="Atenção", message="O campo segundo dever ser selecionado.")
                return False
            elif not cls.second.get().isdigit():
                messagebox.showwarning(title="Atenção", message="Segundo inválida")
                return False
            elif int(cls.second.get()) > 59 or int(cls.second.get()) < 0:
                messagebox.showwarning(title="Atenção", message="Segundo inválida")
                return False
            return True

        def validate_name(cls):
            if cls.name.get() == "" or cls.name.get() is None:
                messagebox.showwarning(title="Atenção", message="O campo nome deve ser preenchido.")
                return False
            return True

        if not validate_source_file(self):
            return False
        elif not validate_destination_path(self):
            return False
        elif not validate_name(self):
            return False
        elif not validate_interval(self):
            return False
        elif not validate_combobox_hour(self):
            return False
        elif not validate_combobox_minute(self):
            return False
        elif not validate_combobox_second(self):
            return False
        return True

    def change_button_action_state(self, value: bool) -> None:
        if value:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'
        else:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'

    def change_form_state(self, value):
        if value:
            self.button_source_file["state"] = "normal"
            self.button_destination_path["state"] = "normal"
            self.entry_interval["state"] = "normal"
            self.combobox_hour["state"] = "normal"
            self.combobox_minute["state"] = "normal"
            self.combobox_second["state"] = "normal"
            self.entry_name["state"] = "normal"
        else:
            self.button_source_file["state"] = "disabled"
            self.button_destination_path["state"] = "disabled"
            self.entry_interval["state"] = "disabled"
            self.combobox_hour["state"] = "disabled"
            self.combobox_minute["state"] = "disabled"
            self.combobox_second["state"] = "disabled"
            self.entry_name["state"] = "disabled"



