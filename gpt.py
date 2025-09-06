from langchain_ollama import OllamaLLM
import sys
import os

# Model seçenekleri (hızdan yavaşa doğru)
MODELS = {
    "fast": "llama3.2:1b",      # En hızlı, küçük model
    "medium": "llama3.2:3b",    # Orta hız ve kalite
    "quality": "llama3.1:8b",   # Yavaş ama kaliteli
    "default": "llama3"         # Varsayılan
}

# Çevre değişkeninden model seçimi (varsayılan: fast)
selected_model = os.getenv("CHAT_MODEL", "default")
model_name = MODELS.get(selected_model, MODELS["default"])

print(f"Model: {model_name} ({selected_model} modu)")

try:
    # Türkçe cevap için optimizasyonlar
    gpt = OllamaLLM(
        model=model_name,
        temperature=0.1,      # Düşük randomness = tutarlı Türkçe
        num_predict=512,      # Kısa Türkçe cevaplar
        num_ctx=4096,        # Context window
        system="Sen Türk bir doktorsun. Sadece Türkçe konuş. İngilizce yasak."
    )
except Exception as e:
    print(f"Ollama bağlantı hatası: {e}")
    print("Ollama servisinin çalıştığından emin olun: 'ollama serve'")
    print(f"Ve {model_name} modelinin yüklü olduğundan emin olun: 'ollama pull {model_name}'")
    sys.exit(1)

def cevapvergpt(prompt, context=""):
    """
    GPT ile soru-cevap fonksiyonu
    Args:
        prompt: Kullanıcı sorusu
        context: PDF'den çıkarılan bağlam metni (opsiyonel)
    """
    try:
        if context:
            # Güçlü Türkçe dil zorlaması
            full_prompt = f"""UYARI: Cevabın %100 Türkçe olmalı. Hiçbir İngilizce kelime kullanma!

Sen Türk bir pediatrik endokrinoloji uzmanısın. Tüm tıbbi terimleri Türkçe karşılıklarıyla kullan.

Kitap bilgileri: {context}

Hasta sorusu: {prompt}

ZORUNLU KURALLAR:
- Sadece Türkçe cevap ver
- İngilizce terim kullanma 
- Tıbbi terimleri Türkçe söyle
- Kısa ve net cevap ver

Türkçe cevap:"""
        else:
            full_prompt = f"""UYARI: Cevabın tamamen Türkçe olmalı!

Sen Türk bir pediatrik endokrinoloji doktorusun. 

Soru: {prompt}

ZORUNLU:
- Sadece Türkçe yaz
- İngilizce kelime yasak
- Kısa cevap ver

Türkçe cevap:"""
        
        response = gpt.invoke(full_prompt)
        
        # Türkçe kontrolü ve düzeltme
        if response and len(response.strip()) > 0:
            # Eğer cevap çok fazla İngilizce içeriyorsa tekrar dene
            english_words = ['the', 'and', 'is', 'are', 'in', 'of', 'to', 'with', 'for', 'on', 'at', 'by']
            english_count = sum(1 for word in english_words if word.lower() in response.lower())
            
            if english_count > 3:  # Çok fazla İngilizce varsa
                # Basit Türkçe cevap ver
                simple_prompt = f"Bu soruya Türkçe tek cümle ile cevap ver: {prompt}"
                response = gpt.invoke(simple_prompt)
        
        return response
        
    except Exception as e:
        return f"Cevap oluşturulurken hata: {e}\nOllama servisinin çalıştığını kontrol edin."

