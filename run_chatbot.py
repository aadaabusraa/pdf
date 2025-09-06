#!/usr/bin/env python3
"""
Pediatrik Endokrinoloji AI Chatbot
Sperling Pediatric Endocrinology kitabını referans alarak soru-cevap sistemi
"""

import os
import sys
try:
    from main import PDFSohbet
except ImportError as e:
    print(f"main.py import hatası: {e}")
    sys.exit(1)

def check_requirements():
    """Gerekli dosya ve servisleri kontrol et"""
    errors = []
    
    # PDF dosyası kontrolü
    pdf_files = [
        "2021 Sperling Pediatric Endocrinology by Mark Sperling.pdf",
        "../2021 Sperling Pediatric Endocrinology by Mark Sperling.pdf",
        "k1.pdf"
    ]
    
    pdf_found = False
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            pdf_found = True
            break
    
    if not pdf_found:
        errors.append("Sperling Pediatric Endocrinology PDF dosyası bulunamadı")
        errors.append("   Dosyayı aichat klasörüne veya üst dizine koyun")
    
    # Ollama kontrolü
    try:
        from langchain_ollama import OllamaLLM
        # Test connection with timeout
        test_llm = OllamaLLM(model="llama3")
        test_response = test_llm.invoke("test")
        print("Ollama servisi çalışıyor")
    except ImportError:
        errors.append("langchain-ollama paketi bulunamadı")
        errors.append("   'pip install langchain-ollama' komutuyla yükleyin")
    except Exception as e:
        errors.append(f"Ollama bağlantı problemi: {e}")
        errors.append("   'ollama serve' komutuyla servisi başlatın")
        errors.append("   'ollama pull llama3' komutuyla modeli indirin")
    
    return errors

def main():
    print("=" * 70)
    print("PEDİATRİK ENDOKRİNOLOJİ AI ASİSTANI")
    print("Sperling Pediatric Endocrinology Referanslı")
    print("=" * 70)
    
    # Sistem kontrolü
    print("\nSistem kontrolleri yapılıyor...")
    errors = check_requirements()
    
    if errors:
        print("\nSistemde problemler var:")
        for error in errors:
            print(error)
        print("\nLütfen problemleri çözün ve tekrar deneyin.")
        return
    
    print("Tüm kontroller başarılı!")
    print("\n" + "="*50)
    print("KULLANIM KLAVUZU:")
    print("• Pediatrik endokrinoloji ile ilgili sorularınızı sorun")
    print("• AI, Sperling kitabındaki bilgileri kullanarak cevap verecek")
    print("• Çıkmak için 'k' yazın")
    print("="*50)
    print()
    
    try:
        # Chatbot'u başlat
        bot = PDFSohbet()
        
        if not bot.pdf_context:
            print("PDF yüklenemedi. Sadece genel sorular cevaplanabilir.\n")
        else:
            print("PDF başarıyla yüklendi! Artık Sperling kitabı referanslı sorular sorabilirsiniz.\n")
        
        # Ana döngü
        while True:
            try:
                print("─" * 50)
                bot.sorun().cevap()
                if bot.soru.lower() == "k":
                    print("\n" + "="*30)
                    print("Görüşmek üzere!")
                    print("="*30)
                    break
                print()
            except KeyboardInterrupt:
                print("\n\nProgram sonlandırıldı.")
                break
            except Exception as e:
                print(f"\nBeklenmeyen hata: {e}")
                break
                
    except Exception as e:
        print(f"Chatbot başlatılamadı: {e}")

if __name__ == "__main__":
    main()