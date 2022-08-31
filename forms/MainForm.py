import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from tkinter import filedialog
import shutil
from widgets.MaskedInt import MaskedInt


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.photoimages = []
        self.start = False
        self.file = None

        self.source_file = ttk.StringVar()
        self.destination_path = ttk.StringVar()
        self.sync_time = ttk.StringVar()
        self.afterid = ttk.StringVar()

        self.entry_sync_time = None
        self.button_action = None
        self.button_source_file = None
        self.button_destination_path = None

        masked_int = MaskedInt()
        self.digit_func = self.register(masked_int.mask_number)

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

        label = ttk.Label(frame, text="Tempo Sincronismo")
        label.grid(row=2, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        self.entry_sync_time = ttk.Entry(frame, width=10, justify="center", textvariable=self.sync_time, validate="key",
                                         validatecommand=(self.digit_func, '%S', '%P', '%d'))
        self.entry_sync_time.grid(row=2, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

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
        file = self.source_file.get()
        self.file = self.destination_path.get() + "/" + file.split("/")[-1]

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
            print(self.file)
            shutil.copy2(self.source_file.get(), self.file)
        except Exception as err:
            print(err)
            messagebox.showerror(title="Erro", message="Erro ao copiar arquivo.")
        finally:
            time = int(self.sync_time.get()) * 1000
            self.afterid.set(self.after(time, self.loop))

    def validate(self):
        def validate_source_file(cls):
            if cls.source_file.get() == "" or cls.source_file.get() is None:
                messagebox.showwarning(title="Atenção", message="Selecione o arquivo de origem.")
                return False
            else:
                return True

        def validate_destination_path(cls):
            if cls.destination_path.get() == "" or cls.destination_path.get() is None:
                messagebox.showwarning(title="Atenção", message="Selecione o diretório de destino.")
                return False
            else:
                return True

        def validate_sync_time(cls):
            if cls.sync_time.get() == "" or cls.sync_time.get() is None:
                messagebox.showwarning(title="Atenção", message="Selecione o tempo de sincronismo.")
                return False
            elif int(cls.sync_time.get()) <= 0:
                messagebox.showwarning(title="Atenção", message="O tempo de sincronismo deve ser maior ou igual a 0.")
                return False
            else:
                return True

        if not validate_source_file(self):
            return False
        elif not validate_destination_path(self):
            return False
        elif not validate_sync_time(self):
            return False
        else:
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
            self.entry_sync_time["state"] = "normal"
        else:
            self.button_source_file["state"] = "disabled"
            self.button_destination_path["state"] = "disabled"
            self.entry_sync_time["state"] = "disabled"


