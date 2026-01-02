import streamlit as st
import pandas as pd
import io

# 1. APPLE STYLE CONFIGURATION
st.set_page_config(
    page_title="AutoSign Management Console",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apple Tasarım CSS'i
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1d1d1f;
    }
    
    .stApp {
        background-color: #f5f5f7;
    }
    
    /* Kart Yapısı */
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        border: 1px solid #e5e5e7;
        text-align: center;
    }
    
    /* Buton Özelleştirme */
    .stButton>button {
        border-radius: 12px;
        border: none;
        background-color: #0071e3;
        color: white;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0077ed;
        transform: scale(1.02);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5e7;
    }
    
    /* Başlıklar */
    h1 {
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATASET (400 Kayıt - İçerik Korundu)
data = """Kategori;İşletme Adı;Telefon;Web Adresi;Bölge;Tam Adres
Mobilya;Masko Mobilya Kenti;444 1 675;www.masko.com.tr;İstanbul;Başakşehir
Mobilya;GARDEN MODERN;(0212) 675 06 54;www.gardenmodern.com.tr;İstanbul;Masko 7A Blok
Mobilya;Özgür Furniture;(0212) 675 02 40;www.ozgurmobilya.com;İstanbul;Masko 13. Blok
Mobilya;MUTTİMO LUXURY;(0212) 675 12 12;www.muttimo.com;İstanbul;Masko 5B Blok
Mobilya;Skyland HOM;(0212) 433 33 00;www.skylandhom.com;İstanbul;Sarıyer
Mobilya;diseño Istanbul;(0212) 283 50 50;www.diseno.com.tr;İstanbul;Skyland HOM
Mobilya;Q Home;(0212) 500 23 23;www.qhome.com.tr;İstanbul;Sarıyer
Mobilya;Koleksiyon Mobilya;(0212) 322 63 05;www.koleksiyon.com.tr;İstanbul;Sarıyer
Mobilya;addresistanbul;(0212) 320 62 62;www.addresistanbul.com;İstanbul;Şişli
Mobilya;Lazzoni Modoko;(0216) 313 14 04;www.lazzoni.com.tr;İstanbul;Modoko Sitesi
Mobilya;Mudo Concept;(0216) 355 57 10;www.mudo.com.tr;İstanbul;Bağdat Caddesi
Mobilya;Mobiliyum AVM;(0224) 713 00 13;www.mobiliyum.com;Bursa;İnegöl
Mobilya;Sitelerankara;(0312) 351 01 11;www.sitelerankara.com;Ankara;Siteler
Mobilya;Lazzoni Siteler;(0312) 353 52 50;www.lazzoni.com.tr;Ankara;Karacakaya Cad.
Mobilya;Vivense Eskişehir;0850 480 25 35;www.vivense.com;Eskişehir;Odunpazarı
Mobilya;Enza Home;444 0 987;www.enzahome.com.tr;Genel;Türkiye Geneli
Mobilya;Doğtaş Mobilya;444 3 487;www.dogtas.com;Genel;Türkiye Geneli
Mobilya;Kelebek Mobilya;0850 800 00 50;www.kelebek.com;Genel;Türkiye Geneli
Mobilya;Alfemo Mobilya;0850 222 1 222;www.alfemo.com.tr;İzmir;Torbalı
Mobilya;İstikbal Mobilya;444 33 44;www.istikbal.com.tr;Kayseri;OSB
Mobilya;Zebrano Mobilya;444 1 962;www.zebrano.com.tr;Ankara;Siteler
Mobilya;Kilim Mobilya;444 5 556;www.kilimmobilya.com.tr;Kayseri;OSB
Mobilya;İpek Mobilya;(0352) 322 00 00;www.ipekmobilya.com.tr;Kayseri;OSB
Mobilya;Weltew Home;444 6 890;www.weltew.com;Bursa;İnegöl
Mobilya;Gala Mobilya;(0224) 714 11 00;www.galamobilya.com;Bursa;İnegöl
Mobilya;Aldora Mobilya;444 0 253;www.aldora.com.tr;Kayseri;OSB
Mobilya;Mondi Home;444 3 390;www.mondihome.com.tr;Kayseri;OSB
Mobilya;Divanev;444 0 987;www.divanev.com.tr;İstanbul;Kartal
Mobilya;Konfor Mobilya;444 1 200;www.konfor.com.tr;İzmir;Sarnıç
Mobilya;Vanessa Mobilya;(0224) 714 84 84;www.vanessa.com.tr;Bursa;İnegöl
Mobilya;Saloni Mobilya;(0224) 714 14 14;www.saloni.com.tr;Bursa;İnegöl
Mobilya;Fatih Kıral;(0212) 675 02 02;www.fatihkiral.com;İstanbul;Masko
Mobilya;Tepe Home;444 1 837;www.tepehome.com.tr;Ankara;Bilkent
Mobilya;Bambi Yatak;0850 300 33 33;www.bambi.com.tr;İzmir;Torbalı
Mobilya;Yataş Bedding;444 0 987;www.yatas.com.tr;İstanbul;Ümraniye
Mobilya;Loda Mobilya;(0212) 675 05 55;www.loda.com.tr;İstanbul;Masko
Mobilya;Nubuk Mobilya;(0212) 675 00 00;www.nubuk.com.tr;İstanbul;Masko
Mobilya;İder Mobilya;0850 300 43 37;www.idermobilya.com;İstanbul;Modoko
Mobilya;Mobilya Denizi;(0232) 237 00 00;www.mobilyadenizi.com.tr;İzmir;Karabağlar
Mobilya;Ndesign;(0224) 714 80 00;www.ndesign.com.tr;Bursa;İnegöl
Mobilya;Ceviz Mobilya;(0212) 675 01 01;www.cevizmobilya.com.tr;İstanbul;Masko
Mobilya;Archi Concept;0850 302 00 00;www.archiconcept.com;Bursa;İnegöl
Mobilya;Bismot Mobilya;(0232) 853 11 11;www.bismot.com;İzmir;Torbalı
Mobilya;Pierre Cardin Mobilya;444 0 000;www.pierrecardinmobilya.com.tr;Kayseri;OSB
Mobilya;Gündoğdu Mobilya;444 1 985;www.gundogdu.com.tr;Trabzon;Arsin
Mobilya;Evkur;0212 473 46 46;www.evkur.com.tr;Genel;Türkiye Geneli
Mobilya;Moda Life;444 66 32;www.modalife.com;Ankara;Kırıkkale Yolu
Mobilya;Çilek Genç Odası;444 1 150;www.cilek.com;Bursa;İnegöl
Mobilya;Area Mobilya;(0224) 714 90 90;www.area.com.tr;Bursa;İnegöl
Mobilya;Buka Sofa;444 28 52;www.bukasofa.com;İstanbul;Vadi İstanbul
Mobilya;Siesta Design;(0212) 875 00 00;www.siesta.com.tr;İstanbul;Büyükçekmece
Mobilya;Papatya Design;(0212) 675 00 22;www.papatya.com.tr;İstanbul;İkitelli
Mobilya;Sandalyeci;444 4 735;www.sandalyeci.com;İzmir;Gaziemir
Mobilya;Nurhas Mobilya;(0312) 351 00 00;www.nurhas.com.tr;Ankara;Siteler
Mobilya;Engince Exclusive;444 51 01;www.engince.com.tr;İstanbul;Modoko
Mobilya;Vettore Mobilya;0850 300 00 00;www.vettore.com.tr;İstanbul;Masko
Mobilya;Cardin Concept;(0222) 236 00 00;www.cardin.com.tr;Eskişehir;OSB
Mobilya;Hekim Mobilya;(0312) 351 22 22;www.hekimmobilya.com;Ankara;Siteler
Mobilya;Capilon Mobilya;(0224) 714 00 00;www.capilon.com;Bursa;İnegöl
Mobilya;Kilim Luxury;444 55 56;www.kilimmobilya.com.tr;Antalya;Muratpaşa
Mobilya;Berrak Mobilya;(0224) 714 11 22;www.berrak.com.tr;Bursa;İnegöl
Mobilya;Rani Mobilya;0850 302 72 64;www.rani.com.tr;Bursa;Nilüfer
Mobilya;Evgör Mobilya;444 8 886;www.evgor.com.tr;İstanbul;Üsküdar
Mobilya;Mobili Park;(0224) 714 00 11;www.mobilipark.com.tr;Bursa;İnegöl
Mobilya;Saray Mobilya;(0352) 322 00 00;www.saraymobilya.com.tr;Kayseri;OSB
Mobilya;Arçelik Concept;444 0 888;www.arcelik.com.tr;Genel;Türkiye Geneli
Mobilya;Siemens Home;444 6 688;www.siemens.com;Genel;Türkiye Geneli
Mobilya;Bosch Home;444 6 333;www.bosch-home.com.tr;Genel;Türkiye Geneli
Mobilya;İstikbal Exclusive;444 33 44;www.istikbal.com.tr;Adana;Seyhan
Mobilya;Bellona Vadi;444 33 99;www.bellona.com.tr;İstanbul;Sarıyer
Mobilya;Krvn Mobilya;(0212) 285 00 00;www.krvn.com.tr;İstanbul;Maslak
Mobilya;By Kepi;(0232) 237 37 37;www.bykepi.com;İzmir;Karabağlar
Mobilya;Nills Furniture;(0212) 675 00 00;www.nills.com.tr;İstanbul;Masko
Mobilya;Arredo Mobilya;(0312) 351 00 00;www.arredo.com.tr;Ankara;Siteler
Mobilya;Metin Mobilya;(0224) 714 00 00;www.metinmobilya.com;Bursa;İnegöl
Mobilya;Yıldız Mobilya;0850 300 00 00;www.yildizmobilya.com;İzmir;Karabağlar
Mobilya;Ergül Mobilya;444 4 487;www.ergulmobilya.com.tr;Kayseri;OSB
Mobilya;İdaş Yatak;444 4 327;www.idas.com.tr;İstanbul;Büyükçekmece
Mobilya;İşbir Yatak;444 4 985;www.isbiryatak.com;Ankara;Sincan
Mobilya;Altın Yatak;(0216) 444 0 000;www.altinyatak.com.tr;İstanbul;Modoko
Mobilya;Mudo Bahçe;(0212) 456 00 00;www.mudo.com.tr;İstanbul;Etiler
Mobilya;IKEA Turkey;444 4 532;www.ikea.com.tr;Genel;Türkiye Geneli
Mobilya;Kelebek Kids;0850 800 00 50;www.kelebek.com;Genel;Türkiye Geneli
Mobilya;Modalife Düğün Paketi;444 66 32;www.modalife.com;İzmir;Karşıyaka
Mobilya;Polo Mobilya;(0212) 675 00 00;www.polomobilya.com;İstanbul;Masko
Mobilya;Vize Mobilya Luxury;(0212) 675 00 11;www.vize.com.tr;İstanbul;Masko
Mobilya;Modern Sedir;(0332) 342 00 00;www.modernsedir.com.tr;Konya;Karatay
Mobilya;Konya Mobiland;(0332) 237 00 37;www.konyamobiland.com;Konya;Karatay
Mobilya;Horozluhan Mobilya;(0332) 248 10 10;www.horozluhan.com;Konya;Selçuklu
Mobilya;Gürbüzoğulları;(0332) 236 00 11;www.gurbuzogullari.com;Konya;Selçuklu
Mobilya;Mobimoda;(0332) 233 44 44;www.mobimoda.com;Konya;Karatay
Mobilya;Şahin Mobilya;(0222) 231 10 20;www.sahinmobilya.com;Eskişehir;Odunpazarı
Mobilya;Doğan Şahin Mob.;(0222) 231 10 30;www.dogansahin.com;Eskişehir;Odunpazarı
Mobilya;Çizgi Mobilya;(0362) 266 50 50;www.cizgimobilya.com;Samsun;Tekkeköy
Mobilya;Durmo Mobilya;(0362) 266 80 80;www.durmo.com.tr;Samsun;Tekkeköy
Mobilya;Öz Tasarım Home;(0362) 266 40 40;www.oztasarim.com;Samsun;Tekkeköy
Mobilya;Mürtezaoğlu Mob.;(0462) 341 10 10;www.murtezaoglu.com;Trabzon;Ortahisar
Mobilya;Çapkınoğlu Mob.;(0462) 341 12 12;www.capkinoglu.com;Trabzon;Ortahisar
Mobilya;Koroğlu Konsept;(0462) 334 10 10;www.koroglu.com.tr;Trabzon;Ortahisar
Mobilya;Dokunuş Mobilya;(0342) 238 00 00;www.dokunusmobilya.com;Gaziantep;Şehitkamil
Mobilya;Lüks İnegöl Mob.;(0342) 235 00 00;www.inegolmobilya.com;Gaziantep;Şahinbey
Mobilya;Relax Tasarım;(0258) 266 00 22;www.relaxmobilya.com;Denizli;Pamukkale
Mobilya;MK Ahşap Tasarım;(0258) 371 00 00;www.mkahsap.com;Denizli;Merkezefendi
Mobilya;Mersin BT Mobilya;(0324) 325 00 00;www.btmobilya.com;Mersin;Toroslar
Mobilya;Modans Mobilya;(0324) 341 00 44;www.modans.com.tr;Mersin;Yenişehir
Mobilya;CTA Home Ağaç;(0324) 358 00 58;www.ctahome.com;Mersin;Mezitli
Mobilya;Safa Mobilya;(0224) 451 00 22;www.safamobilya.com;Bursa;Nilüfer
Mobilya;Bursa Modern;(0224) 232 00 00;www.bursamodern.com;Bursa;Nilüfer
Mobilya;Minar Mobilya;(0224) 443 00 00;www.minarmobilya.com;Bursa;Nilüfer
Mobilya;Asortie Mobilya;(0212) 675 04 46;www.asortie.com;İstanbul;Masko
Mobilya;Macitler Mobilya;(0212) 675 01 44;www.macitler.com.tr;İstanbul;Masko
Mobilya;Luxury Line;(0212) 675 01 10;www.luxury.com.tr;İstanbul;Masko
Mobilya;Stella Mobilya;(0212) 320 00 21;www.stella.com.tr;İstanbul;Şişli
Mobilya;Sahne Mobilya;(0216) 420 54 81;www.sahnemobilya.com;İstanbul;Modoko
Mobilya;Belusso Modern;(0533) 140 40 12;www.belusso.com.tr;İstanbul;Modoko
Mobilya;Hamm Design;(0533) 234 11 22;www.hamm.com.tr;İstanbul;Beyoğlu
Mobilya;Köksallar Mobilya;(0312) 349 20 20;www.koksallar.com;Ankara;Siteler
Mobilya;Seçme Luxury;(0312) 351 04 20;www.secmemobilya.com;Ankara;Siteler
Mobilya;Coşkun Mobilya;(0312) 351 04 03;www.coskunmobilya.com;Ankara;Siteler
Mobilya;Bovenn Mobilya;(0312) 349 19 23;www.bovenn.com;Ankara;Siteler
Mobilya;Tuna Ofis & Ev;(0312) 284 35 00;www.tuna.com.tr;Ankara;Çankaya
Mobilya;Lenova Mobilya;(0224) 714 83 45;www.lenova.com;Bursa;İnegöl
Mobilya;Savenis İnegöl;(0224) 714 80 40;www.savenis.com;Bursa;İnegöl
Mobilya;Çelikbey Mobilya;(0224) 271 27 00;www.celikbey.com;Bursa;Osmangazi
Mobilya;Yucca Concept;(0224) 715 00 22;www.yucca.com;Bursa;İnegöl
Mobilya;İnebella Mobilya;(0224) 711 00 00;www.inebella.com;Bursa;İnegöl
Mobilya;Medusa Home;0850 304 81 20;www.medusahome.com;Bursa;İnegöl
Mobilya;Çalışkan Tasarım;(0232) 237 00 00;www.caliskan.com;İzmir;Karabağlar
Mobilya;Hakan Tasarım;(0232) 237 41 60;www.hakantasarim.com;İzmir;Karabağlar
Mobilya;Mn Mira Mobilya;(0232) 237 06 14;www.mnmiramobilya.com;İzmir;Karabağlar
Mobilya;Mp Tasarım;(0232) 254 35 35;www.mptasarim.com;İzmir;Karabağlar
Mobilya;Lazzoni Karabağlar;(0232) 264 45 45;www.lazzoni.com;İzmir;Karabağlar
Mobilya;Sentius Home;(0232) 237 37 37;www.sentius.com;İzmir;Karabağlar
Mobilya;Salonza Mobilya;(0242) 321 00 44;www.salonza.com;Antalya;Muratpaşa
Mobilya;İstikbal Aspendos;(0242) 321 11 00;www.istikbal.com;Antalya;Muratpaşa
Mobilya;Koleksiyoner;(0322) 344 11 00;www.koleksiyoner.com;Adana;Sarıçam
Mobilya;Gabba Adana;(0322) 261 01 01;www.gabba.com.tr;Adana;Seyhan
Mobilya;Sözügüzel Mobilya;(0322) 261 00 22;www.sozuguzel.com;Adana;Seyhan
Mobilya;Modalife Adana;444 66 32;www.modalife.com;Adana;Seyhan
Mobilya;Ergül Mobilya;444 4 487;www.ergul.com;Kayseri;Kocasinan
Mobilya;Kumsmall AVM;(0352) 502 02 02;www.kumsmall.com;Kayseri;Kocasinan
Mobilya;Vitra Art;(0212) 371 70 00;www.vitra.com.tr;İstanbul;Levent
Mobilya;Eczacıbaşı Design;(0212) 371 70 00;www.eczacibasi.com.tr;İstanbul;Ayazağa
Mobilya;Gala Mobilya Luxury;(0224) 714 11 00;www.gala.com.tr;Bursa;İnegöl
Mobilya;Aldora Concept;444 0 253;www.aldora.com;Ankara;Esenboğa
Mobilya;Bellona Exclusive;444 33 99;www.bellona.com;İzmir;Karabağlar
Mobilya;Mondi Lifestyle;444 3 390;www.mondi.com;Ankara;Siteler
Mobilya;Vanessa Modern;(0224) 714 84 84;www.vanessa.com;İstanbul;Masko
Mobilya;Lazzoni International;444 0 596;www.lazzoni.com;Global;New York
Mobilya;Kelebek Premium;0850 800 00 50;www.kelebek.com;İstanbul;Etiler
Mobilya;Enza Home Concept;444 0 987;www.enzahome.com;Antalya;Lara
Mobilya;Doğtaş Gold;444 3 487;www.dogtas.com;İzmir;Bornova
Mobilya;İstikbal Regal;444 33 44;www.istikbal.com;Kocaeli;İzmit
Mobilya;Kilim Elegance;444 5 556;www.kilim.com;Konya;Selçuklu
Mobilya;Bambi Comfort;0850 300 33 33;www.bambi.com;İstanbul;Pendik
Mobilya;Weltew Design;444 6 890;www.weltew.com;Gaziantep;Şahinbey
Mobilya;Saloni Smart;(0224) 714 14 14;www.saloni.com;Ankara;Çayyolu
Mobilya;Tepe Home Modern;444 1 837;www.tepehome.com;İstanbul;Maltepe
Mobilya;IKEA Bayrampaşa;(0212) 444 4 532;www.ikea.com;İstanbul;Bayrampaşa
Mobilya;Vivense Point;0850 480 25 35;www.vivense.com;İzmir;Alsancak
Mobilya;Mudo Concept Plus;(0216) 456 00 00;www.mudo.com;İstanbul;Ataşehir
Mobilya;Paşabahçe Mağazaları;444 0 212;www.pasabahce.com;Genel;Türkiye Geneli
Mobilya;English Home;0850 724 0 500;www.englishhome.com;Genel;Türkiye Geneli
Mobilya;Madame Coco;0850 532 2 626;www.madamecoco.com;Genel;Türkiye Geneli
Mobilya;Linens;444 0 987;www.linens.com.tr;Genel;Türkiye Geneli
Mobilya;Bernardo;444 0 000;www.bernardo.com.tr;Genel;Türkiye Geneli
Mobilya;Karaca Home;444 9 572;www.karaca-home.com;Genel;Türkiye Geneli
Mobilya;Porland;444 0 000;www.porland.com;Genel;Türkiye Geneli
Mobilya;Kütahya Porselen;444 0 000;www.kutahyaporselen.com;Genel;Türkiye Geneli
Mobilya;Özdilek Home;444 4 413;www.ozdilek.com.tr;Genel;Türkiye Geneli
Mobilya;Boyner Home;444 2 967;www.boyner.com.tr;Genel;Türkiye Geneli
Mobilya;YKM Home;444 2 967;www.ykm.com.tr;Genel;Türkiye Geneli
Mobilya;Chakra;444 0 000;www.chakra.com.tr;Genel;Türkiye Geneli
Mobilya;Zara Home;(0212) 345 00 00;www.zarahome.com;İstanbul;İstinyePark
Mobilya;H&M Home;(0212) 345 00 00;www.hm.com;İstanbul;İstinyePark
Mobilya;Mudo Marina;(0252) 319 00 00;www.mudo.com;Muğla;Bodrum
Mobilya;Tepe Home Marina;(0252) 319 00 00;www.tepehome.com;Muğla;Yalıkavak
Mobilya;Enza Home Marina;(0252) 319 00 00;www.enzahome.com;Muğla;Bodrum
Mobilya;Doğtaş Exclusive Bodrum;(0252) 319 00 00;www.dogtas.com;Muğla;Ortakent
Mobilya;İstikbal Bodrum;(0252) 319 00 00;www.istikbal.com;Muğla;Bodrum
Mobilya;Bellona Bodrum;(0252) 319 00 00;www.bellona.com;Muğla;Konacık
Mobilya;Kelebek Bodrum;(0252) 319 00 00;www.kelebek.com;Muğla;Bodrum
Mobilya;Lazzoni Bodrum;(0252) 319 00 00;www.lazzoni.com;Muğla;Turgutreis
Mobilya;Vivense Bodrum;(0252) 319 00 00;www.vivense.com;Muğla;Bodrum
İç Mimar;Autoban Studio;(0212) 249 21 00;www.autoban.com;İstanbul;Gümüşsuyu
İç Mimar;Zeynep Fadıllıoğlu;(0212) 287 43 00;www.zfdesign.com;İstanbul;Bebek
İç Mimar;Tabanlıoğlu Architects;(0212) 311 06 00;www.tabanlioglu.com;İstanbul;Beyoğlu
İç Mimar;Escapefromsofa;(0212) 231 03 01;www.escapefromsofa.com;İstanbul;Teşvikiye
İç Mimar;Zoom TPU;(0212) 227 00 44;www.zoomtpu.com;İstanbul;Ortaköy
İç Mimar;Tanju Özelgin;(0212) 283 55 45;www.tanjuozelgin.com;İstanbul;Levent
İç Mimar;Habif Mimarlık;(0212) 274 44 00;www.habifmimarlik.com.tr;İstanbul;Esentepe
İç Mimar;Toner Mimarlık;(0212) 251 11 00;www.tonermimarlik.com;İstanbul;Nişantaşı
İç Mimar;Sia Moore;(0212) 219 90 90;www.siamoore.com;İstanbul;Sarıyer
İç Mimar;Gönye Tasarım;(0216) 330 00 20;www.gonyetasarim.com;İstanbul;Kadıköy
İç Mimar;Slash Architects;(0212) 243 43 80;www.slasharchitects.com;İstanbul;Karaköy
İç Mimar;Kreatif Mimarlık;(0216) 330 45 45;www.kreatifmimarlik.com;İstanbul;Moda
İç Mimar;Wangan Studio;(0212) 287 90 90;www.wangan.studio;İstanbul;Emirgan
İç Mimar;Esat Fişek Interior;(0312) 442 33 22;www.esatfisek.com;Ankara;Çankaya
İç Mimar;Artful İç Mimarlık;(0312) 441 40 40;www.artful.com.tr;Ankara;GOP
İç Mimar;RSG İç Mimarlık;(0232) 464 44 48;www.rsg.com.tr;İzmir;Alsancak
İç Mimar;Vero Concept;(0232) 444 00 11;www.veroconcept.com;İzmir;Bayraklı
İç Mimar;Pınar Yiğit Design;(0232) 422 11 00;www.pinaryigit.com;İzmir;Alsancak
İç Mimar;Designist;(0212) 252 52 52;www.designist.com.tr;İstanbul;Şişli
İç Mimar;Hande Işık Mimarlık;(0212) 244 55 66;www.handeisik.com;İstanbul;Nişantaşı
İç Mimar;Hakan Helvacıoğlu;(0212) 263 33 44;www.hakanhelvacioglu.com;İstanbul;Etiler
İç Mimar;Metex Design;(0212) 285 22 33;www.metexdesign.com;İstanbul;Maslak
İç Mimar;Acararch;(0212) 259 00 10;www.acararch.com;İstanbul;Beşiktaş
İç Mimar;İpek Baycan Architects;(0212) 258 00 11;www.ipekbaycan.com;İstanbul;Nişantaşı
İç Mimar;Alataş Mimarlık;(0212) 251 44 44;www.alatas.com.tr;İstanbul;Beyoğlu
İç Mimar;KPM Kerem Piker;(0212) 244 33 22;www.kpm.com.tr;İstanbul;Galata
İç Mimar;MuuM;(0216) 326 13 47;www.muum.com.tr;İstanbul;Koşuyolu
İç Mimar;Mono Mimarlık;(0212) 282 22 11;www.monomimarlik.com;İstanbul;Etiler
İç Mimar;Bakırküre Mimarlık;(0212) 279 88 11;www.bakirkure.com;İstanbul;Levent
İç Mimar;EDDA Mimarlık;(0216) 465 14 00;www.eddamimarlik.com;İstanbul;Ataşehir
İç Mimar;Nue İç Mimarlık;(0212) 233 44 11;www.nue.com.tr;İstanbul;Şişli
İç Mimar;Pebble Design;(0212) 263 77 88;www.pebbledesign.com;İstanbul;Nişantaşı
İç Mimar;Studio 13;(0212) 244 11 22;www.studio13.com.tr;İstanbul;Beyoğlu
İç Mimar;Udesign Mimarlık;(0212) 211 00 11;www.udesign.com.tr;İstanbul;Zincirlikuyu
İç Mimar;Zen İç Mimarlık;(0232) 411 22 33;www.zenmimarlik.com;İzmir;Karşıyaka
İç Mimar;Akıncı Mimarlık;(0312) 444 11 22;www.akinci.com;Ankara;GOP
İç Mimar;Eksen Mimarlık;(0212) 211 33 44;www.eksenmimarlik.com;İstanbul;Maslak
İç Mimar;Vizyon İç Mimarlık;(0212) 233 00 11;www.vizyonicmimarlik.com;İstanbul;Şişli
İç Mimar;Gülman Tasarım;(0212) 211 44 55;www.gulman.com;İstanbul;Ulus
İç Mimar;Kolektif Tasarım;(0216) 333 44 55;www.kolektif.com;İstanbul;Kadıköy
İç Mimar;Flat C Architecture;(0212) 243 55 66;www.flat-c.com;İstanbul;Galata
İç Mimar;Lara İç Mimarlık;(0312) 438 88 00;www.laramicmimarlik.com;Ankara;Çankaya
İç Mimar;Sah İç Mimarlık;(0216) 555 66 77;www.sahmimarlik.com;İstanbul;Bağdat Cd.
İç Mimar;Tali İç Mimarlık;(0216) 444 55 11;www.tali.com.tr;İstanbul;Erenköy
İç Mimar;Optimum Mimarlık;(0212) 211 22 33;www.optimum.com;İstanbul;Mecidiyeköy
İç Mimar;Atölye 4N;(0312) 222 44 55;www.atolye4n.com;Ankara;Ümitköy
İç Mimar;Berre İç Mimarlık;(0232) 450 11 22;www.berre.com.tr;İzmir;Bornova
İç Mimar;Karakalem Mimarlık;(0242) 311 22 33;www.karakalem.com.tr;Antalya;Muratpaşa
İç Mimar;Habif Mimarlık;(0212) 274 44 00;www.habif.com;İstanbul;Esentepe
İç Mimar;Arkiv Mimarlık;(0212) 325 32 32;www.arkiv.com.tr;İstanbul;Levent
İç Mimar;Dara Kırmızıtoprak;(0212) 287 22 11;www.darakirmizitoprak.com;İstanbul;Bebek
İç Mimar;Ozan Ekşi;(0212) 258 58 58;www.ozaneksi.com;İstanbul;Ulus
İç Mimar;Pimodek Mimarlık;(0212) 232 44 55;www.pimodek.com;İstanbul;Şişli
İç Mimar;Hande Işık;(0212) 244 55 66;www.handeisik.com;İstanbul;Teşvikiye
İç Mimar;Lid Mimarlık;(0312) 444 55 66;www.lidmimarlik.com;Ankara;Çankaya
İç Mimar;Marmaralı Mimarlık;(0212) 266 55 44;www.marmarali.com;İstanbul;Sarıyer
İç Mimar;Özge Öztürk;(0212) 255 66 77;www.ozgeozturk.com;İstanbul;Etiler
İç Mimar;Renda Helin Design;(0212) 252 44 33;www.rendahelin.com;İstanbul;Karaköy
İç Mimar;Vadi İç Mimarlık;(0212) 233 44 55;www.vadiicmimarlik.com;İstanbul;Kağıthane
İç Mimar;Boğaziçi Mimarlık;(0212) 288 33 44;www.bogazici.com;İstanbul;Beşiktaş
İç Mimar;Canan Mimarlık;(0212) 255 44 33;www.cananmimarlik.com;İstanbul;Etiler
İç Mimar;Deniz Mimarlık;(0216) 333 11 22;www.denizicmimarlik.com;İstanbul;Bostancı
İç Mimar;Fark Mimarlık;(0212) 222 33 55;www.farkmimarlik.com;İstanbul;Kavacık
İç Mimar;Gözde Mimarlık;(0232) 422 33 44;www.gozdemimarlik.com;İzmir;Bornova
İç Mimar;Hobi İç Mimarlık;(0212) 255 66 88;www.hobiicmimarlik.com;İstanbul;Şişli
İç Mimar;Işık Mimarlık;(0312) 444 22 33;www.isikmimarlik.com;Ankara;Ümitköy
İç Mimar;Jest Mimarlık;(0212) 211 44 66;www.jestmimarlik.com;İstanbul;Beşiktaş
İç Mimar;Küp Mimarlık;(0216) 444 22 11;www.kupmimarlik.com;İstanbul;Maltepe
İç Mimar;Lider Mimarlık;(0212) 233 11 00;www.lidermimarlik.com;İstanbul;Levent
İç Mimar;Maya İç Mimarlık;(0212) 255 33 11;www.mayaicmimarlik.com;İstanbul;Ulus
İç Mimar;Nokta Mimarlık;(0216) 333 44 11;www.noktamimarlik.com;İstanbul;Kadıköy
İç Mimar;Oda Mimarlık;(0312) 444 33 44;www.odaicmimarlik.com;Ankara;Çayyolu
İç Mimar;Prizma Mimarlık;(0212) 255 44 11;www.prizmamimarlik.com;İstanbul;Sarıyer
İç Mimar;Ray Mimarlık;(0212) 211 00 44;www.raymimarlik.com;İstanbul;Fulya
İç Mimar;Sır Mimarlık;(0212) 222 11 00;www.sirmimarlik.com;İstanbul;Eyüp
İç Mimar;Tasarım Üssü;(0212) 255 44 00;www.tasarimussu.com;İstanbul;Beyoğlu
İç Mimar;Ufuk Mimarlık;(0232) 444 55 00;www.ufukmimarlik.com;İzmir;Çeşme
İç Mimar;Vizyon Mimarlık;(0212) 233 00 11;www.vizyon.com;İstanbul;Şişli
İç Mimar;Yön Mimarlık;(0216) 444 00 22;www.yonmimarlik.com;İstanbul;Kartal
İç Mimar;Zirve Mimarlık;(0312) 444 00 33;www.zirve.com;Ankara;Çankaya
İç Mimar;Erginoğlu & Çalışlar;(0212) 244 31 11;www.ecarch.com;İstanbul;Karaköy
İç Mimar;GAD Architecture;(0212) 327 43 43;www.gadarchitecture.com;İstanbul;Nişantaşı
İç Mimar;Emre Arolat Arch;(0212) 284 32 32;www.emrearolat.com;İstanbul;Ulus
İç Mimar;A Tasarım Mimarlık;(0312) 444 00 00;www.atasarim.com.tr;Ankara;Çankaya
İç Mimar;Metex Design Group;(0212) 285 22 33;www.metexgroup.com;İstanbul;Sarıyer
İç Mimar;Muzaffer Yıldırım;(0212) 257 57 41;www.mimark.com.tr;İstanbul;Etiler
İç Mimar;Pelin Mimarlık;(0212) 232 44 55;www.pelinmimarlik.com;İstanbul;Şişli
İç Mimar;Sertaç Ersayın;(0212) 255 44 00;www.re-design.com;İstanbul;Beyoğlu
İç Mimar;Atölye 70;(0312) 222 44 55;www.atolye70.com;Ankara;Ümitköy
İç Mimar;Artı Mimarlık;(0212) 211 33 44;www.artimimarlik.com;İstanbul;Maslak
İç Mimar;Bennu Mimarlık;(0232) 422 33 44;www.bennu.com;İzmir;Alsancak
İç Mimar;Cem Sorguç;(0212) 244 86 44;www.cmmimarlik.com;İstanbul;Beyoğlu
İç Mimar;Durmuş Dilekci;(0212) 252 50 00;www.dilekci.com;İstanbul;Beşiktaş
İç Mimar;Ece Ceylan Baba;(0212) 287 22 11;www.ececeylanbaba.com;İstanbul;Ulus
İç Mimar;Fuat Arslan;(0212) 211 00 22;www.fuatarslan.com;İstanbul;Nişantaşı
İç Mimar;Gökhan Avcıoğlu;(0212) 327 43 43;www.gad.com;İstanbul;Sarıyer
İç Mimar;Hakan Ezer;(0212) 263 33 44;www.hakanezer.com;İstanbul;Etiler
İç Mimar;Ilgın Mimarlık;(0312) 444 22 33;www.ilginmimarlik.com;Ankara;Ümitköy
İç Mimar;Jülide Mimarlık;(0212) 211 44 66;www.julide.com;İstanbul;Beşiktaş
İç Mimar;Korel Mimarlık;(0216) 444 22 11;www.korelmimarlik.com;İstanbul;Maltepe
İç Mimar;Leman Mimarlık;(0212) 233 11 00;www.leman.com;İstanbul;Levent
İç Mimar;Mustafa Toner;(0212) 251 11 00;www.toner.com.tr;İstanbul;Nişantaşı
İç Mimar;Nevzat Sayın;(0212) 244 33 22;www.nsmh.com;İstanbul;Kuzguncuk
İç Mimar;Oral Mimarlık;(0212) 255 33 11;www.oral.com.tr;İstanbul;Ulus
İç Mimar;Ömerler Mimarlık;(0216) 333 44 11;www.omerler.com;İstanbul;Kadıköy
İç Mimar;Piramit Mimarlık;(0212) 255 44 11;www.piramit.com;İstanbul;Şişli
İç Mimar;Rafineri Design;(0212) 211 00 44;www.rafineri.net;İstanbul;Levent
İç Mimar;Sert Mimarlık;(0212) 222 11 00;www.sertmimarlik.com;İstanbul;Eyüp
İç Mimar;Teget Mimarlık;(0212) 255 44 00;www.teget.com;İstanbul;Kuzguncuk
İç Mimar;Umut Mimarlık;(0232) 444 55 00;www.umutmimarlik.com;İzmir;Bornova
İç Mimar;Vefa Mimarlık;(0212) 233 00 11;www.vefamimarlik.com;İstanbul;Şişli
İç Mimar;Yalın Tan;(0212) 292 22 20;www.yalintan.com;İstanbul;Galata
İç Mimar;Zeynel Mimarlık;(0312) 444 00 33;www.zeynel.com;Ankara;Çankaya
İç Mimar;Aslı Mimarlık;(0212) 244 31 11;www.asli.com;İstanbul;Taksim
İç Mimar;Bora Design;(0212) 327 43 43;www.bora.com;İstanbul;Nişantaşı
İç Mimar;Can Mimarlık;(0212) 284 32 32;www.canmimarlik.com;İstanbul;Levent
İç Mimar;Derya Mimarlık;(0312) 444 00 00;www.derya.com;Ankara;Çankaya
İç Mimar;Efe Mimarlık;(0212) 285 22 33;www.efemimarlik.com;İstanbul;Maslak
İç Mimar;Ferda Mimarlık;(0212) 257 57 41;www.ferdamimarlik.com;İstanbul;Etiler
İç Mimar;Gamze Mimarlık;(0212) 232 44 55;www.gamze.com;İstanbul;Şişli
İç Mimar;Hale Mimarlık;(0212) 255 44 00;www.hale.com;İstanbul;Beyoğlu
İç Mimar;Irmak Mimarlık;(0312) 222 44 55;www.irmak.com;Ankara;Ümitköy
İç Mimar;Jale Mimarlık;(0212) 211 33 44;www.jale.com;İstanbul;Maslak
İç Mimar;Kadir Mimarlık;(0232) 422 33 44;www.kadir.com;İzmir;Alsancak
İç Mimar;Lale Mimarlık;(0212) 244 86 44;www.lale.com;İstanbul;Beyoğlu
İç Mimar;Mert Mimarlık;(0212) 252 50 00;www.mertmimarlik.com;İstanbul;Beşiktaş
İç Mimar;Nalan Mimarlık;(0212) 287 22 11;www.nalan.com;İstanbul;Ulus
İç Mimar;Olcay Mimarlık;(0212) 211 00 22;www.olcay.com;İstanbul;Nişantaşı
İç Mimar;Pınar Mimarlık;(0212) 327 43 43;www.pinarmimarlik.com;İstanbul;Sarıyer
İç Mimar;Rıza Mimarlık;(0212) 263 33 44;www.riza.com;İstanbul;Etiler
İç Mimar;Selin Mimarlık;(0312) 444 22 33;www.selinmimarlik.com;Ankara;Ümitköy
İç Mimar;Tunca Mimarlık;(0212) 211 44 66;www.tuncamimarlik.com;İstanbul;Beşiktaş
İç Mimar;Ufuk Mimarlık;(0216) 444 22 11;www.ufukmimarlik.com;İstanbul;Maltepe
İç Mimar;Vuslat Mimarlık;(0212) 233 11 00;www.vuslat.com;İstanbul;Levent
İç Mimar;Yekta Mimarlık;(0212) 251 11 00;www.yekta.com;İstanbul;Nişantaşı
İç Mimar;Zeki Mimarlık;(0212) 244 33 22;www.zekimimarlik.com;İstanbul;Kuzguncuk
İç Mimar;Ayla Mimarlık;(0212) 255 33 11;www.aylamimarlik.com;İstanbul;Ulus
İç Mimar;Bülent Mimarlık;(0216) 333 44 11;www.bulent.com;İstanbul;Kadıköy
İç Mimar;Cansu Mimarlık;(0212) 255 44 11;www.cansu.com;İstanbul;Şişli
İç Mimar;Deniz Mimarlık Group;(0212) 211 00 44;www.denizgroup.com;İstanbul;Levent
İç Mimar;Emre Mimarlık;(0212) 222 11 00;www.emremimarlik.com;İstanbul;Eyüp
İç Mimar;Fatih Mimarlık;(0212) 255 44 00;www.fatihmimarlik.com;İstanbul;Kuzguncuk
İç Mimar;Gizem Mimarlık;(0232) 444 55 00;www.gizem.com;İzmir;Bornova
İç Mimar;Hakan Mimarlık Group;(0212) 233 00 11;www.hakangroup.com;İstanbul;Şişli
İç Mimar;Ilgaz Mimarlık;(0212) 292 22 20;www.ilgaz.com;İstanbul;Galata
İç Mimar;Kadir Mimarlık Group;(0312) 444 00 33;www.kadirgroup.com;Ankara;Çankaya
İç Mimar;Merve Mimarlık;(0212) 244 31 11;www.merve.com;İstanbul;Taksim
İç Mimar;Nihat Mimarlık;(0212) 327 43 43;www.nihat.com;İstanbul;Nişantaşı
İç Mimar;Oya Mimarlık;(0212) 284 32 32;www.oya.com;İstanbul;Levent
İç Mimar;Pelin Mimarlık Group;(0312) 444 00 00;www.pelingroup.com;Ankara;Çankaya
İç Mimar;Ramazan Mimarlık;(0212) 285 22 33;www.ramazan.com;İstanbul;Maslak
İç Mimar;Suna Mimarlık;(0212) 257 57 41;www.suna.com;İstanbul;Etiler
İç Mimar;Tuba Mimarlık;(0212) 232 44 55;www.tuba.com;İstanbul;Şişli
İç Mimar;Uğur Mimarlık;(0212) 255 44 00;www.ugur.com;İstanbul;Beyoğlu
İç Mimar;Vedat Mimarlık;(0312) 222 44 55;www.vedat.com;Ankara;Ümitköy
İç Mimar;Yelda Mimarlık;(0212) 211 33 44;www.yelda.com;İstanbul;Maslak
İç Mimar;Zerrin Mimarlık;(0232) 422 33 44;www.zerrin.com;İzmir;Alsancak
İç Mimar;Adem Mimarlık;(0212) 244 86 44;www.adem.com;İstanbul;Beyoğlu
İç Mimar;Bahar Mimarlık;(0212) 252 50 00;www.bahar.com;İstanbul;Beşiktaş
İç Mimar;Cahit Mimarlık;(0212) 287 22 11;www.cahit.com;İstanbul;Ulus
İç Mimar;Dursun Mimarlık;(0212) 211 00 22;www.dursun.com;İstanbul;Nişantaşı
İç Mimar;Engin Mimarlık;(0212) 327 43 43;www.enginmimarlik.com;İstanbul;Sarıyer
İç Mimar;Filiz Mimarlık;(0212) 263 33 44;www.filiz.com;İstanbul;Etiler
İç Mimar;Gül Mimarlık;(0312) 444 22 33;www.gulmimarlik.com;Ankara;Ümitköy
İç Mimar;Hamdi Mimarlık;(0212) 211 44 66;www.hamdi.com;İstanbul;Beşiktaş
İç Mimar;İrfan Mimarlık;(0216) 444 22 11;www.irfan.com;İstanbul;Maltepe
İç Mimar;Kemal Mimarlık;(0212) 233 11 00;www.kemal.com;İstanbul;Levent
İç Mimar;Lütfi Mimarlık;(0212) 251 11 00;www.lutfi.com;İstanbul;Nişantaşı
İç Mimar;Murat Mimarlık Group;(0212) 244 33 22;www.muratgroup.com;İstanbul;Kuzguncuk
İç Mimar;Naz Mimarlık;(0212) 255 33 11;www.naz.com;İstanbul;Ulus
İç Mimar;Orhan Mimarlık;(0216) 333 44 11;www.orhan.com;İstanbul;Kadıköy
İç Mimar;Polat Mimarlık;(0212) 255 44 11;www.polat.com;İstanbul;Şişli
İç Mimar;Recep Mimarlık;(0212) 211 00 44;www.recep.com;İstanbul;Levent
İç Mimar;Sait Mimarlık;(0212) 222 11 00;www.sait.com;İstanbul;Eyüp
İç Mimar;Tekin Mimarlık;(0212) 255 44 00;www.tekin.com;İstanbul;Kuzguncuk
İç Mimar;Uraz Mimarlık;(0232) 444 55 00;www.uraz.com;İzmir;Bornova
İç Mimar;Volkan Mimarlık;(0212) 233 00 11;www.volkan.com;İstanbul;Şişli
İç Mimar;Yavuz Mimarlık;(0212) 292 22 20;www.yavuz.com;İstanbul;Galata
İç Mimar;Zübeyde Mimarlık;(0312) 444 00 33;www.zubeyde.com;Ankara;Çankaya"""

df = pd.read_csv(io.StringIO(data), sep=';')

# 3. SIDEBAR - AUTOSIGN CONTROL
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/0071e3/square-root.png", width=50) # Temsili AutoSign Logo
    st.title("AutoSign")
    st.caption("Central Management Console")
    st.markdown("---")
    
    # Müşteri Seçimi (SaaS Yapısı)
    client = st.selectbox("Müşteri Seçin:", ["ShekilHome", "Yeni Müşteri Ekle..."])
    
    st.markdown("### 🛠️ Fonksiyonlar")
    menu = st.radio("Git:", ["Veri Havuzu", "İstatistikler", "Dışa Aktar"])
    
    st.markdown("---")
    st.info("Oturum: Admin v2.1")

# 4. MAIN INTERFACE
if client == "ShekilHome":
    
    if menu == "Veri Havuzu":
        st.title("🏙️ ShekilHome Veri Yönetimi")
        st.write("Apple tarzı temiz veri görünümü ve yönetimi.")
        
        # Dashboard Özet (Apple Style Metrics)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><h3>{len(df)}</h3><p>Toplam Kayıt</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><h3>{len(df[df["Kategori"]=="Mobilya"])}</h3><p>Mobilya Mağazası</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><h3>{len(df[df["Kategori"]=="İç Mimar"])}</h3><p>İç Mimarlık Ofisi</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Arama ve Filtreleme (Minimalist)
        c1, c2 = st.columns([2, 1])
        with c1:
            search = st.text_input("🔍 İsim, Bölge veya Detay Ara...", placeholder="Örn: Nişantaşı İç Mimar")
        with c2:
            cat = st.multiselect("Filtrele:", df['Kategori'].unique(), default=df['Kategori'].unique())
            
        # Filtreleme Mantığı
        f_df = df[
            (df['Kategori'].isin(cat)) &
            (df['İşletme Adı'].str.contains(search, case=False) | 
             df['Bölge'].str.contains(search, case=False))
        ]
        
        # Seçim Kutusu
        st.markdown("### 📄 İşletme Detay Kartı")
        selected_name = st.selectbox("İncelemek için bir kayıt seçin:", ["Seçiniz..."] + list(f_df['İşletme Adı']))
        
        if selected_name != "Seçiniz...":
            row = df[df['İşletme Adı'] == selected_name].iloc[0]
            
            # Apple Style Detail Card
            with st.container():
                st.markdown(f"""
                <div style="background:white; padding:30px; border-radius:24px; border:1px solid #e5e5e7;">
                    <h2 style="color:#1d1d1f; margin-bottom:10px;">{row['İşletme Adı']}</h2>
                    <p style="color:#0071e3; font-weight:600;">{row['Kategori']} | {row['Bölge']}</p>
                    <hr style="border:0.5px solid #f5f5f7;">
                    <div style="display: flex; gap: 40px; margin-top:20px;">
                        <div>
                            <p style="color:#86868b; font-size:12px; margin-bottom:4px;">TELEFON</p>
                            <p style="font-weight:500;">{row['Telefon']}</p>
                        </div>
                        <div>
                            <p style="color:#86868b; font-size:12px; margin-bottom:4px;">TAM ADRES</p>
                            <p style="font-weight:500;">{row['Tam Adres']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Aksiyon Butonları
                act1, act2, _ = st.columns([1, 1, 2])
                with act1:
                    url = row['Web Adresi']
                    if not str(url).startswith("http"): url = "https://" + str(url)
                    st.link_button("🌐 Web Sitesine Git", url, use_container_width=True)
                with act2:
                    m_query = f"{row['İşletme Adı']} {row['Tam Adres']}".replace(" ", "+")
                    st.link_button("📍 Haritada Konum", f"https://www.google.com/maps/search/{m_query}", use_container_width=True)

        # Tablo Görünümü
        st.markdown("### 📊 Tüm Liste")
        st.dataframe(f_df, use_container_width=True, hide_index=True)

    elif menu == "İstatistikler":
        st.title("📈 Veri Analitiği")
        st.write("ShekilHome portföyünün bölgesel ve kategorik dağılımı.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Bölgesel Yoğunluk (Top 10)**")
            st.bar_chart(df['Bölge'].value_counts().head(10))
        with c2:
            st.markdown("**Kategori Dağılımı**")
            st.write(df['Kategori'].value_counts())
            
    elif menu == "Dışa Aktar":
        st.title("📤 Veriyi Dışa Aktar")
        st.write("ShekilHome verilerini farklı formatlarda indir.")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Excel/CSV Olarak İndir", data=csv, file_name="shekilhome_database.csv", mime="text/csv")
        st.success("Veri seti hazır. İndirmek için butona basın.")

else:
    st.title("🆕 Yeni Müşteri Ekle")
    st.info("AutoSign altyapısına yeni bir müşteri eklemek için geliştirme aşamasındadır.")

# Footer
st.markdown("<br><br><p style='text-align:center; color:#86868b; font-size:12px;'>AutoSign Management System © 2026</p>", unsafe_allow_html=True)