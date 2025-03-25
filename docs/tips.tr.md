# Profesyonel Kodlama İpuçları - Türkçe

## `nmap.xml` dosyasının kullanımı nedir?
Artık `nmap.xml` dosyasının kullanımını sorabilirsiniz. AI'nın bu sınıf/modül ile bir şey uygulamasını istediğinizde, ona sınıfın kodunu veya belgelerini vermeniz gerekir. Çoğu AI modeli, XML belgelerini çok iyi ve doğru bir şekilde okuyabilir.

## Neden stabil bir koda ulaştığımda depoyu saklamalıyım?
Kodun stabil bir hale geldiğinde depoyu saklamaya ÇALIŞ. Çünkü kodu bozabiliriz ve çok fazla yanlış düzeltme yüzünden çalıştıramayabilir ya da tamir edemeyebiliriz. Bu yüzden her stabil noktada bir geri yükleme noktası kaydet, böylece yanlış kodlarla projeni çökertirsen geri dönebilirsin.

## Neden her geliştirme/hata ayıklama/düzeltme/iyileştirme aşamasında test yapmalıyım?
1 saatlik geliştirme sonrası kodu çalıştırıyorum ve hatalar peş peşe geliyor. Bu yüzden her geliştirme/hata ayıklama/düzeltme/iyileştirme aşamasında test yapmanızı söyledim. Daha sonra UNIT_TEST'ler, mantık testleri ve akış testleri hakkında konuşmak için bir video kaydedeceğim. Kodlamada teknikler var, ama ben AI ile tüm olası yolları en hızlı şekilde nasıl test edeceğinizi kaydedeceğim.

## Neden dizini oluşturduktan sonra git'e commit etmeden önce `.gitkeep` ekledim?
Çünkü git normalde boş dizinleri commit ve push sırasında depoya göndermez. Bu yüzden projemizde bu dizine ihtiyacımız varsa ve geçici değilse, içine bir dosya eklememiz gerekir. Ben genellikle `.gitkeep` ekleyerek yeni dizini git'e zorla commit ve push ile depoya göndermeyi standart olarak kullanıyorum. Dizine dosya ekledikten sonra ise `.gitkeep`'i kaldırıyorum.