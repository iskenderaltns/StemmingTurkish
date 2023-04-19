### Python ile Türkçe kelimelerin kökünü bulma

Bildiğiniz üzere Türkçe sondan eklemeli ve bünyesinde çok fazla başka dillerden kelime barındıran bir dildir. Bu sebepten ötürü İngilizce veya Fransızca dillerinde olduğu gibi kolay bir şekilde kök bulmak zor bir iştir. Bu çalışmamda minimum database kullanarak yapabildiğim kadar Türkçe kelimelerin kökeni buldum. 

### Bu projenin amaçları:
 - Kelime kökü bulma
 - Farklı ekler almış ama kökleri aynı olan kelimeleri tek bir kelime(kök) altında toplamak istiyorum.  

#### Eklenecek kurallar <img src="https://user-images.githubusercontent.com/86206193/233212314-1e7d51e9-d80e-4f13-a260-488a41429156.jpg" alt="pp" width="10%" height="10%" align ='right'/>

- Ünlü düşmesi (Örn: Kısmı --> Kısım)
- Bazı eklerin kontrol edilmesi gerkiyor (Belirtme Hal Eki, Genel olarak sıfatların ve isimlerin sonlarına gelen ekler)
- ...

#### Eklenen özellikler
- İngilizce klavye yüzünden yazılamayan üöşğıç harflerinin oluşturduğu kelime çeşitliliği kaldırıldı ([StemmedVisualization](https://github.com/iskenderaltns/StemmingTurkish/blob/main/StemmedVisualization.ipynb)--> possibleMatch)
  - örneğin: Eğer datamızda urun, ürün, ürun, urün kelimeleri varsa bunlar tek bir kelime altında toplanacak. Fakat bu keime ürün olmak zorunda değil. Bu olasılıklardan hangisinin (yani ürün mü doğru yoksa urun mu ) doğru olduğunu kestirmek zor bir iş. 
- yapılan eylemin olumlu mu olumsuz mu olduğunu anlama ([stemmingTurkish](https://github.com/iskenderaltns/StemmingTurkish/blob/main/stemmingTurkish.py) --> stemming --> yorum satırıda olan kodu aktifleştirmeniz gerekiyor) 

   > if self.negative_words: result.append('-negative-')
  - örneğin: yapmamalıydı -- > -negatif- yap (burada kelimenin kökünün yap olduğunu lakin cümle içerisinde olumsuz kullanıldığını belirtiyor. Türkçe duygu analizi için bir iyileştirme)
 
- Gereksiz yazılan bazı harfleri algılama ve silme ([stemmingTurkish](https://github.com/iskenderaltns/StemmingTurkish/blob/main/stemmingTurkish.py) --> control_end_2)
  - örneğin : ürünnn -- > ürün, elllbise --> elbise
 
 Örnek testler: 
   Deneme için trendyol sitesinden bazı yorumlar aldım. 3 yorumun sonucu: 
   

<p align="center">
  <img src="https://user-images.githubusercontent.com/86206193/233211636-2165fbf1-099c-46a6-9e2f-4a69ffd2838c.png" alt="pp" width="30%" height="40%"/>
  <img src="https://user-images.githubusercontent.com/86206193/233211641-7e860227-3818-4490-a9cd-42590d37f87b.png" alt="pp" width="30%" height="40%"/>
  <img src="https://user-images.githubusercontent.com/86206193/233211643-7c4f5de5-fc15-41f5-895d-e0afefccccde.png"" alt="pp" width="30%" height="40%"/>
</p>
   
### Note :
Bu bulunan köklerin %100 doğru olmasını beklenmemeli. Bu projenin her ne kadar amacı kök bulmak olsa da diğer bir amacı ise kelimeleri olabildiğince bir kelime altında toplamak. 
Örneğin: vardı, varmak, varmış, varacak ... kelimelerini var adı altında toplamak benim için tatmin edici bir sonuç. NLP mantığında kelimeleri bir vektöre çevirirken ağırlık(örn: kelime sayısı/count) büyük bir önem taşır. 

Şimdi içinde 570k dan fazla kelime olan önceden eğitilmiş bir gloveTurkısh sözlüğünü kullanarak kök bulmadan önce ve sonra ne kadar kelimeyle uğraşmam gerektiğini ve ne kadar kelime yakaladığımın sonucuna bakalım. ([EmbeddingTest sonuçları ](https://github.com/iskenderaltns/StemmingTurkish/blob/main/EmbeddingTest.ipynb)) 

<p align="center">
  <img src="https://user-images.githubusercontent.com/86206193/233216130-1ede560b-17e3-4f1e-ba34-75e776231af8.png" alt="p1p" width="40%" height="50%"/>
  <img src="https://user-images.githubusercontent.com/86206193/233216125-fbb14c7f-b657-4b06-a962-a6ad0b4c11ca.png"" alt="p2p" width="30%" height="40%"/>
</p>

Burada gördüğünüz üzere kelimelerin kökeni bulunmadan önce 2808 kelimenin 2717 tanesini yakalayabiliyoruz. 
Kelimelerin kökünü bulduktan sonra ise toplam kelime sayımız 1678 oluyor ve bunlardan 1347 tanesini yakalayabiliyoruz. Sonuç daha da güzel olabilir. Bu testi trendyoldan aldığım 2k'dan fazla ürün yorumlarıyla yaptım. Haliyle eksik veya yanlış yazılmış kelimeler de var. Buradan çıkan sonuç ise bine yakın kelimenin köklerini bularak bunları köklerinin altında topladım. Bu yapacağım eğitimde(train-test) daha hızlı ve daha doğru bir sonuç verebilmesini sağlar. 

şimdi ise bunları WordCloud ile görselleştirelim. Bunu yaparken bazı duraksama kelimelerini (stop words) kaldırdım.
#### ilk olarak stemming yapmadan en sık geçen kelimelere bakalım.
<p align="center">
  <img src="https://user-images.githubusercontent.com/86206193/233217845-bc6fab8f-9a01-4144-9f0e-fdeb2b43a73f.png" alt="p1p" width="45%" height="30%"/>
</p>

Gördüğünüz gibi beğendim, alınmalı vs. kelimeler biraz rahatsız ediyor. 
#### Şimdi ise stemming yaptıktan sonraki en sık geçen kelimelere bakalım. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/86206193/233218574-47bb5d6b-b863-4b2b-b346-0e66afdd517c.png" alt="p1p" width="45%" height="30%"/>
</p>


Öneri: Database biraz daha sıfat ve isim yükleyerek doğruluk oranı arttırılabilir. (Bu sıfat ve isimler daha çok sonunda ek varmış gibi görünenlerden olacak. Örneğin kadın ve sandın kelimeleri, bu kelimeler -dın ile bitiyor. Bilgisayar bunu ise 2.tekil şahıs geçmiş zaman olarak algılıyor. Bu durumda kök olarak -ka ve -san verecek. Fakat datamızda kadın kelimesi olduğu için bunu yapamıyor.)   


