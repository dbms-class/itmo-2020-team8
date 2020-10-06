# itmo-2020-team8

# 1 
спортсмен	{
  - спортсмен_id ????
  - номер карточки unique	
  - имя	
  - пол	
  - рост	
  - вес
  - возраст	
  - делегация/страна_id	
  - адрес_id
  - волонтер_id
}
делегация	{
  - делегация_id
  - руководитель_id
  - адрес_id	
}
руководитель {
  - руководитель_id
  - имя	
  - телефон	
}		
обьект{
  - обьект_id
  - адрес_id not unique
  - тип
  - имя (optional)
}	
	
адрес	{
  - адрес_id
  - улица	
  - дом	
}







# 2 

Соревнование(
  id
  название
  дата
  время
  объект
)

Cписки людей на соревнованании(
  id соревнованания
  id спортсмена/волонтера?
)

Медаль(
  спортсмен
  id соревнование
  номинал медали
)

Площадки(
  спорт
  объект
)


---- 

# 3 Volunteers

Volunteer
 - id    (primary key)
 - idcard ( unique number)
 - name  (string, varchar)
 - phone (varchar)

VolunteerTask
 - id          (primary key)
 - Transport$reg_number (foreign key)
 - datetime    (datetime)
 - description (textarea)

Transport
 - reg_number (primary key)
 - capacity