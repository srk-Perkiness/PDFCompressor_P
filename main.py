"""PDF Compressor - Desktop GUI Application."""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from compressor import compress_pdf


class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Compressor")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 400) // 2
        self.root.geometry(f"500x400+{x}+{y}")

        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="PDF Compressor",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=(0, 20))

        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF File", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))

        self.select_btn = ttk.Button(
            file_frame,
            text="Browse...",
            command=self.select_file
        )
        self.select_btn.pack(side=tk.LEFT)

        self.file_label = ttk.Label(
            file_frame,
            text="No file selected",
            foreground="gray"
        )
        self.file_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # Compression level section
        level_frame = ttk.LabelFrame(main_frame, text="Compression Level", padding="10")
        level_frame.pack(fill=tk.X, pady=(0, 15))

        self.compression_var = tk.StringVar(value="Medium")
        levels = ["Low", "Medium", "High"]

        for level in levels:
            rb = ttk.Radiobutton(
                level_frame,
                text=level,
                variable=self.compression_var,
                value=level
            )
            rb.pack(side=tk.LEFT, padx=(0, 20))

        # Description labels for compression levels
        desc_frame = ttk.Frame(level_frame)
        desc_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(
            desc_frame,
            text="Low: Preserve quality | Medium: Balanced | High: Max compression",
            foreground="gray",
            font=("Helvetica", 9)
        ).pack()

        # Compress button
        self.compress_btn = ttk.Button(
            main_frame,
            text="Compress PDF",
            command=self.start_compression,
            style="Accent.TButton"
        )
        self.compress_btn.pack(pady=(0, 15))

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode="indeterminate",
            length=400
        )
        self.progress.pack(pady=(0, 15))

        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(
            status_frame,
            text="Select a PDF file to compress",
            wraplength=420,
            justify=tk.CENTER
        )
        self.status_label.pack(expand=True)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )

        if file_path:
            self.selected_file = file_path
            filename = Path(file_path).name
            if len(filename) > 40:
                filename = filename[:37] + "..."
            self.file_label.config(text=filename, foreground="black")
            self.status_label.config(text=f"Ready to compress: {filename}")

    def start_compression(self):
        if not self.selected_file:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return

        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "Selected file no longer exists.")
            return

        # Ask for output location
        input_path = Path(self.selected_file)
        default_name = f"{input_path.stem}_compressed.pdf"

        output_path = filedialog.asksaveasfilename(
            title="Save Compressed PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            initialdir=input_path.parent,
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not output_path:
            return

        # Disable UI and start progress
        self.set_ui_state(False)
        self.progress.start(10)
        self.status_label.config(text="Compressing... Please wait.")

        # Run compression in background thread
        thread = threading.Thread(
            target=self.compress_thread,
            args=(self.selected_file, output_path)
        )
        thread.daemon = True
        thread.start()

    def compress_thread(self, input_path, output_path):
        try:
            level = self.compression_var.get().lower()
            result = compress_pdf(input_path, output_path, level)

            self.root.after(0, lambda: self.compression_complete(result, output_path))
        except Exception as e:
            self.root.after(0, lambda: self.compression_error(str(e)))

    def compression_complete(self, result, output_path):
        self.progress.stop()
        self.set_ui_state(True)

        # Format sizes nicely
        orig = result['original_size']
        comp = result['compressed_size']
        orig_str = f"{orig:.2f} MB" if orig >= 1 else f"{orig * 1024:.0f} KB"
        comp_str = f"{comp:.2f} MB" if comp >= 1 else f"{comp * 1024:.0f} KB"

        reduction = result['reduction_percent']
        if reduction > 0:
            reduction_str = f"Reduced by {reduction}%"
        elif reduction < 0:
            reduction_str = f"Size increased by {abs(reduction)}%"
        else:
            reduction_str = "No size change"

        status_text = (
            f"Done!\n\n"
            f"Original: {orig_str}\n"
            f"Compressed: {comp_str}\n"
            f"{reduction_str}\n\n"
            f"Saved to: {Path(output_path).name}"
        )

        self.status_label.config(text=status_text)

    def compression_error(self, error_msg):
        self.progress.stop()
        self.set_ui_state(True)
        self.status_label.config(text=f"Error: {error_msg}")
        messagebox.showerror("Compression Error", f"An error occurred:\n{error_msg}")

    def set_ui_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.select_btn.config(state=state)
        self.compress_btn.config(state=state)


def main():
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
