https://useinsider.com/careers/quality-assurance/  bu sayfada "See All QA Jobs" butonuna tıkladıktan sonra açılan yeni sayfadaki dropdown seçiminde,  
location dropdown ununa ilk kez tıklanıldığında altta ekstra yeni bir buton açılıyor belli bir süre sonra bekleyip dropdown u kapatıp tekrar açtığınızda liste yüklenmiş oluyor. 
Ben hem bu case in kodunu yazdım hem de sayfa ilk açıldığında 9 saniye kadar listenin yüklenmesini bekleyip öyle location seçimini yapabileceğiniz kodu yazdım. 
Test kodunda default olarak ilk test case i görebilirsiniz ama diğer 9 saniye beklemeli olan case i de kontrol etmek isterseniz test_others_conditions.py 'de  
yorum satırına aldığım qajobs_page2.py dosyasını aktifleştirebilirsiniz.


Ayrıca aynı sayfada departman dropdown'unda Quality Assurance otomatik olarak sonradan sayfada yükleniyor ama ben yine de kod tarafında 
tekrar listeden bu seçimi dropdown'dan yaptım.
