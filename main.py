from forms.MainForm import MainForm
import ttkbootstrap as ttk


if __name__ == '__main__':
    app = ttk.Window(
        title="Copy File",
        resizable=(False, False)
    )
    MainForm(app)

    app.mainloop()
