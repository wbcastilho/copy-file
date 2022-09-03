import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import filedialog
from widgets.MaskedEntry import MaskedEntry
from pathlib import Path
import datetime
import shutil


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.photoimages = []
        self.start = False
        self.intime = False

        self.source_file = ttk.StringVar()
        self.destination_path = ttk.StringVar()
        self.hour = ttk.StringVar()
        self.minute = ttk.StringVar()
        self.second = ttk.StringVar()
        self.name = ttk.StringVar()
        self.afterid = ttk.StringVar()

        self.hour_values = []
        self.minute_values = []
        self.second_values = []

        self.combobox_hour = None
        self.combobox_minute = None
        self.combobox_second = None
        self.entry_name = None
        self.button_action = None
        self.button_source_file = None
        self.button_destination_path = None
        self.label_state = None
        self.label_state_copy = None
        self.label_last_date = None

        masked_entry = MaskedEntry()
        self.number_func = self.register(masked_entry.mask_number)
        self.entry_func = self.register(masked_entry.mask_entry)

        self.init_combobox()
        self.associate_icons()
        self.create_buttonbar()
        self.create_form_frame()
        self.create_status_frame()

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

    def create_form_frame(self):
        label_frame = ttk.Labelframe(self, text='Cópia')
        label_frame.pack(fill="x", padx=10, pady=(10, 5))

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=(15, 20))

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

        self.entry_name = ttk.Entry(frame, width=50, textvariable=self.name, validate="key",
                                    validatecommand=(self.entry_func, '%P', '%d', '30'))
        self.entry_name.grid(row=2, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

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

    def create_status_frame(self):
        label_frame = ttk.Labelframe(self, text='Status', )
        label_frame.pack(fill="x", padx=10, pady=(5, 20))

        frame_size = ttk.Frame(label_frame, width=70)
        frame_size.pack()

        frame = ttk.Frame(frame_size, borderwidth=1, relief="sunken", width=100)
        frame.pack(fill="both", padx=10, pady=(10, 20))

        label = ttk.Label(frame, text=" Descrição", font='Arial 8 bold', width=40, bootstyle="inverse-primary")
        label.grid(row=0, column=0, sticky=ttk.W)

        label = ttk.Label(frame, text=" Status", font='Arial 8 bold', width=30, bootstyle="inverse-primary")
        label.grid(row=0, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Execução")
        label.grid(row=1, column=0, sticky=ttk.W)

        self.label_state = ttk.Label(frame, text=" Parado", font='Arial 8 bold', bootstyle="danger")
        self.label_state.grid(row=1, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Situação da última cópia")
        label.grid(row=2, column=0, sticky=ttk.W)

        self.label_state_copy = ttk.Label(frame, text=" -", font='Arial 8 bold', bootstyle="danger")
        self.label_state_copy.grid(row=2, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Data da última cópia realizada")
        label.grid(row=3, column=0, sticky=ttk.W)

        self.label_last_date = ttk.Label(frame, text=" -", font='Arial 8 bold', bootstyle="danger")
        self.label_last_date.grid(row=3, column=1, sticky=ttk.W)

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
                self.start = True
                self.change_action_state(False)
                self.after(0, self.loop)
        else:
            self.start = False
            self.change_action_state(True)
            self.after_cancel(self.afterid.get())

    def loop(self):
        try:
            current_date = datetime.datetime.now()
            if self.hour.get() == current_date.strftime("%H") and self.minute.get() == current_date.strftime("%M"):
                if not self.intime:
                    self.intime = True
                    file = f"{self.destination_path.get()}/{self.name.get()}{current_date.strftime('%d_%m_%y')}.txt"
                    shutil.copy2(self.source_file.get(), file)
                    self.change_state_of_label_state_copy(True)
                    self.show_datetime_in_label_last_date(current_date)
                    print(file)
            else:
                self.intime = False
        except Exception:
            self.intime = False
            self.change_state_of_label_state_copy(False)
        finally:
            one_second = 1000
            self.afterid.set(self.after(one_second, self.loop))

    def change_state_of_label_state_copy(self, value: bool):
        if value:
            self.label_state_copy["bootstyle"] = "success"
            self.label_state_copy["text"] = " OK"
        else:
            self.label_state_copy["bootstyle"] = "danger"
            self.label_state_copy["text"] = " Falha"

    def show_datetime_in_label_last_date(self, current_date):
        self.label_last_date["bootstyle"] = "success"
        self.label_last_date["text"] = current_date.strftime('%d/%m/%y %H:%M:%S')

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

        def validate_hour(cls):
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

        def validate_minute(cls):
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

        def validate_second(cls):
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
        elif not validate_hour(self):
            return False
        elif not validate_minute(self):
            return False
        elif not validate_second(self):
            return False
        return True

    def change_action_state(self, value):
        def change_button_action_state(cls) -> None:
            if value:
                cls.button_action['image'] = 'play'
                cls.button_action['text'] = 'Iniciar'
            else:
                cls.button_action['image'] = 'stop'
                cls.button_action['text'] = 'Parar'

        def change_state_of_label_state(cls):
            if value:
                cls.label_state["bootstyle"] = "danger"
                cls.label_state["text"] = " Parado"
            else:
                cls.label_state["bootstyle"] = "success"
                cls.label_state["text"] = " Rodando"

        def change_state_of_form_widgets(cls):
            if value:
                cls.button_source_file["state"] = "normal"
                cls.button_destination_path["state"] = "normal"
                cls.combobox_hour["state"] = "normal"
                cls.combobox_minute["state"] = "normal"
                cls.combobox_second["state"] = "normal"
                cls.entry_name["state"] = "normal"
            else:
                self.button_source_file["state"] = "disabled"
                self.button_destination_path["state"] = "disabled"
                self.combobox_hour["state"] = "disabled"
                self.combobox_minute["state"] = "disabled"
                self.combobox_second["state"] = "disabled"
                self.entry_name["state"] = "disabled"

        change_button_action_state(self)
        change_state_of_form_widgets(self)
        change_state_of_label_state(self)

