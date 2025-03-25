# Profesyonel Kodlama İpuçları - Türkçe

## `nmap.xml` dosyasının kullanımı nedir?
Artık `nmap.xml` dosyasının kullanımını sorabilirsiniz. AI'nın bu sınıf/modül ile bir şey uygulamasını istediğinizde, ona sınıfın kodunu veya belgelerini vermeniz gerekir. Çoğu AI modeli, XML belgelerini çok iyi ve doğru bir şekilde okuyabilir.

## Neden stabil bir koda ulaştığımda depoyu saklamalıyım?
Kodun stabil bir hale geldiğinde depoyu saklamaya ÇALIŞ. Çünkü kodu bozabiliriz ve çok fazla yanlış düzeltme yüzünden çalıştıramayabilir ya da tamir edemeyebiliriz. Bu yüzden her stabil noktada bir geri yükleme noktası kaydet, böylece yanlış kodlarla projeni çökertirsen geri dönebilirsin.

## Neden her geliştirme/hata ayıklama/düzeltme/iyileştirme aşamasında test yapmalıyım?
1 saatlik geliştirme sonrası kodu çalıştırıyorum ve hatalar peş peşe geliyor. Bu yüzden her geliştirme/hata ayıklama/düzeltme/iyileştirme aşamasında test yapmanızı söyledim. Daha sonra UNIT_TEST'ler, mantık testleri ve akış testleri hakkında konuşmak için bir video kaydedeceğim. Kodlamada teknikler var, ama ben AI ile tüm olası yolları en hızlı şekilde nasıl test edeceğinizi kaydedeceğim.

## Neden dizini oluşturduktan sonra git'e commit etmeden önce `.gitkeep` ekledim?
Çünkü git normalde boş dizinleri commit ve push sırasında depoya göndermez. Bu yüzden projemizde bu dizine ihtiyacımız varsa ve geçici değilse, içine bir dosya eklememiz gerekir. Ben genellikle `.gitkeep` ekleyerek yeni dizini git'e zorla commit ve push ile depoya göndermeyi standart olarak kullanıyorum. Dizine dosya ekledikten sonra ise `.gitkeep`'i kaldırıyorum.

## Neden önce kullanıcı dostu bir UX altyapısı oluşturmalıyım?
Uyguladığım UX'ten memnun değilim. Bu yüzden ileriye gitmeden önce, tüm ekranlarda kullanacağımız, havalı ve kullanıcı dostu bir UX altyapısı oluşturalım. Elemanlar ve görünümler, UX dostu ve psikolojik olarak rahatsız edici olmayan renkler kullanmalı; renk kombinasyonları ve düzenlemeler de buna uygun olmalı. El yazısı gibi düzensiz fontlar, imza, bazı başlıklar veya alıntılar gibi çok nadir özel durumlar dışında iyi bir uygulama değildir.

## AI'ya neden uygulamasını ve hatalarını kontrol etmesini istemeliyim?
Prompt'ta, uygulamasını ve sonucunu kontrol etmesini istedim; bu, AI'nın uygulamasını ve hatalarını tekrar gözden geçirmesini sağlar. (Buna AI modellerini düşündürme diyoruz.)

## AI modelleri uzun kod üretiminde eksik kod ürettiğinde ne yapmalıyım?
Bazı durumlarda, özellikle uzun kod üretimlerinde, AI modelleri kodun bazı parçalarını değiştirir ve `(// mevcut fonksiyon)`, `(// diğer fonksiyonlar)`, `(// değişken değerlerinin özet listesi)` gibi notlar ekleyerek eksik kod üretir ve bizden değişiklik yapmamızı ister. Bu durumlarda, AI'dan tüm özellikleri, mantığı ve akışı koruyarak tam dosyayı üretmesini isteyin. Eğer kod çok büyükse, modüler hale getirip ayrı modüllere bölmesini sağlayın.

## Sohbet çok uzadığında ve GROK kafası karıştığında ne yapmalıyım?
Sohbet çok uzadı, GROK kafası karışıyor, çok fazla düşünmesi gerekiyor... Çok uzun bağlamlardan sonra bu hedeflere ulaşmak için yeni bir sohbete geçmeyi öneriyorum, ancak belirli giriş mesajlarıyla:  
- Gerekli uygulanan kodları (özellikle standart temel sınıflar, temalar, kullanılan sınıflar, ...) sağlayın.  
Böylece AI modeli nerede olduğumuzu bilir ve bizim uyguladığımız yöntemlerden farklı yeni çözümler aramaya gitmez. Aksi takdirde çakışmalar olur, yanlış çıktılar üretilir veya daha önce uyguladığımız parçaları yeniden kodlamamıza neden olur.