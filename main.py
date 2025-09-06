from gpt import cevapvergpt
from scrape import get_pdf_chunks
import os
import sys

class PDFSohbet:
    def __init__(self, pdf_path=None):
        self.pdf_context = ""
        self.pdf_path = pdf_path or "n1.pdf"
        self.load_pdf()
    
    def load_pdf(self):
        # Check if file exists in current directory or parent directory
        if not os.path.exists(self.pdf_path):
            parent_path = os.path.join("..", self.pdf_path)
            if os.path.exists(parent_path):
                self.pdf_path = parent_path
            else:
                print(f"PDF dosyası bulunamadı: {self.pdf_path}")
                print("Lütfen PDF dosyasının doğru konumda olduğundan emin olun.")
                return
        
        try:
            print(f"{self.pdf_path} dosyası yükleniyor...")
            chunks = get_pdf_chunks(self.pdf_path)
            if chunks:
                self.pdf_context = "\n".join(chunks)
                print(f"PDF başarıyla yüklendi! {len(chunks)} parça halinde işlendi.")
            else:
                print("PDF yüklenemedi - metin çıkarılamadı.")
        except Exception as e:
            print(f"PDF yükleme hatası: {e}")
    
    def sorun(self):
        self.soru = input("Sorunuzu alalım (k1.pdf dosyasına göre cevaplayacağım): ")
        return self
    
    def cevap(self):
        if self.soru.lower() != "k":
            try:
                if self.pdf_context:
                    # Hızlı yanıt için context boyutunu küçült
                    max_context = 2000  # Küçük context = hızlı yanıt
                    limited_context = self.pdf_context[:max_context]
                    cevap1 = cevapvergpt(self.soru, limited_context)
                    print("\nPediatric Endocrinology kitabına dayalı cevap:")
                    print("-" * 50)
                    print(cevap1)
                else:
                    cevap1 = cevapvergpt(self.soru)
                    print("\nGenel cevap:")
                    print("-" * 50)
                    print(cevap1)
            except Exception as e:
                print(f"\nCevap verirken hata oluştu: {e}")
                print("Ollama servisinin çalıştığından emin olun: 'ollama serve'")
        return self

def main():
    print("=" * 60)
    print("Pediatrik Endokrinoloji AI Asistanı")
    print("Pediatric Endocrinology kitabı referanslı")
    print("=" * 60)
    print("Çıkmak için 'k' yazın\n")
    
    # Initialize chatbot once
    bot = PDFSohbet()
    
    if not bot.pdf_context:
        print("⚠️  PDF yüklenemedi. Sadece genel sorular cevaplanabilir.\n")
    
    while True:
        try:
            bot.sorun().cevap()
            if bot.soru.lower() == "k":
                print("\n" + "=" * 30)
                print("Görüşmek üzere!")
                print("=" * 30)
                break
            print("\n" + "-" * 60 + "\n")
        except KeyboardInterrupt:
            print("\n\nProgram sonlandırıldı.")
            break
        except Exception as e:
            print(f"\nBeklenmeyen hata: {e}")
            break

if __name__ == "__main__":
    main()