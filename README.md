# Норвежско-русский словарь
## Задачи
* Обкачать (норвежско-русский словарь)[http://norwegian_russian.academic.ru/].
* Адаптировать XML-разметку (TEI)[http://www.tei-c.org/index.xml] в соответствии с особенностями словаря.
* Создать XML-файл со всеми статьями словаря в формате TEI.

## Результаты

* `download_dictionary.py` обкачивает словарь. Создается папка `articles`, туда записываются статьи.
* Макет шаблона статьи словаря в формате TEI находится в `xml_template.xml`.
* `process_txt_1.py` и `process_txt_2.py` чистят статьи от артефактов и расставляют теги.
* XML-файл со всеми статьями словаря создается с помощью `make_main_xml.py`
* Исправлены ошибки оригинальной разметки, например: 
```
<p><span class="dic_example">lide avbrekk ( — по)терпеть ущерб</span></p>
```

* Некоторые транскрипции относятся к значениям, а не к статье в целом – записаны в `<note>`.
* В словаре есть пометы, которые относятся к переводу, а не к самому слову:

	*vare*
	*I -en (-a), -er*
	*1) товар, pl товары*
 Они размечены так: *товар, <lbl>pl</lbl> товары*.
 Есть спорные случаи, когда непонятно, к оригиналу или к переводу относятся пометки (*pl* и *пр.*).

* Разные значение слова могут иметь разное словоизменение. Например:
 
 *peppermynte*
 *-a(-en)*
 *1) бот. мята перечная*
 *2) pl -er*
 *мятные лепёшки*
 Сейчас такие случаи размечены в `<note>`: `<gramGrp><num>pl</num><note>-er</note></gramGrp>`.

* Помета *обычно или чаще pl* размечена в `<note>`.
* Для словоизменения могут быть приведены несколько форм с грамматическими показателями. Например:

 *vår*
 *II pron (n vårt, pl våre)*
 *наш, наша (наше, наши)*
 Такие случаи размечены следующим образом: `<inflection><orth>n vårt, pl våre</orth></inflection>`.

## Issues
* Все переводы оформлены через `<text>`, а не `<quote>`, потому что нет консенсуса, как их оформлять.
* Пока нет пояснений к сокращениям `<lbl type="popup"></lbl>`.
* У тегов для особенностей употребления (кроме <lbl>) сейчас нет атрибута `type`. В словаре встречаются следующие пометки:

 редко → `<usg type="plev"></usg>` (частотность - preference level (‘chiefly’, ‘usually’, etc.)) 
 исп. диал. → `<usg type="geo"></usg>` (geographic area)
 уст. → `<usg type="time"></usg>` (temporal, historical era (‘archaic’, ‘old’, etc.)) 
 ав., авт., авто, анат., арт., археол., архит., астр., библ., банк., бизн., биол., бирж., бот., бухг., вет., воен., геогр., геод., геол., геом., геофиз., горн., грам., дип., ж.д., жив., зоол., инф., информ., иск., ист., истор., ихт., каргтогр., карт.#карты, ком., комп., косм., кул., лес., лесн., лингв., лит., лог., малярн., мат., матем., мед, мед., метал., метеор., мех., механ., мин., минер., миф., мор., муз., нефт., нефтегаз., океаногр., орнит., пищ., пласт., полигр., полим., полит., психол., радио, рел., рыб., солн., спорт., стр., страх., студ., театр., телеком., телеф., тех., техн., типогр., топ., торг., фарм., физ., фил., филол., филос, филос., фин., фон., фото, хим, хим., церк., школ., эк., экол., экон, экон., эл., эл.тех., этн., юр. → `<usg type="dom"></usg>` (domain, сфера деятельности)
 разг., фольк., посл. (пословица), поэт., погов. → `<usg type="reg"></usg>` (register = книжн, разг)
 презр., шутл., перен., груб., ирон., ласк., прям., букв., пренебр., вульг., фам., перен → `<usg type="style"></usg>` (style (figurative, literal, etc.) + ирон., негативн., положит.)

* Словообразование и словоизменение (“от <word>”) размечено в `<note>`. Например, превосходная степень размечена так: `<gramGrp><note>superl от stor</note></gramGrp>`.
* Не совсем понятно, как описывать такие случаи:

 *waggon lit*
 *|vagoŋ'li:|*
 *( — pl waggon lits)*
 *ж.-д. спальный вагон*
 Сейчас *pl* и *waggon lits* размечены в `<inflection>`.

* В некоторых случаях сохраняется авторское двоеточие в конце перевода. Например:

 *2) при умножении:*
 *to ganger to er fire — дважды два - четыре*
 *en ad gangen — по одному (не все разом)*
 Просто удалить его нельзя, потому что оно несет смысловую нагрузку.