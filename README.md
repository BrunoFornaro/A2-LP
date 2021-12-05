# Trabalho LP - Site Mercadinhx - A2

Trabalho realizado para a disciplina de Linguagens de Programação dos cursos de Ciência de Dados e Inteligência Artificial e Matemática Aplicada (FGV/EMAp). 

## O site

O [Mercadinhx] é um site que visa a conexão entre o consumidor e o mercado, implementando um sistema sólido que permite a visualização da disponibilidade, localização na prateleira e preço das mercadorias. Possibilita-se, assim, um planejamento prévio das compras, proporcionando uma ida mais rápida e econômica ao mercado.
Além disso, conta com uma assinatura premium que permite ao cliente selecionar os produtos que deseja, pagar pelo próprio site e apenas ir buscar no mercado sua cesta de produtos pronta.


## Integrantes

- Bruno Pereira Fornaro  - B44398
- Daniel Ambrosim Falqueto - B43618
- Lorenzo Aguiar de Alencastro Guimarães - B44407
- Vanessa Berwanger Wille - B43918

## Alterações no site

- O site foi convertido para ser usado com o Django, utilizando a linguagem de templates do Django (DTL).

- Foi criado um banco de dados (com alguns dados próximos de reais, alguns enviesados e outros aleatórios com coerência). A geração dos dados foi feita com código python (`gerar_dados.py`) e a população do banco foi feita com uma conversão dos dados para um JSON válido e comandos no terminal para popular o banco do Django. A estruturado (modelo) e população do banco foi feita utilizando Django (banco de dados sqlite3 que o Django oferece).

- As páginas 'lista_de_produtos' e 'produtos' se tornaram dinâmicas. Utilizando o mesmo html as páginas renderizam os diferentes tipos de seções ou produtos. As URLs dessas páginas passam por um redirecionamento para o resultado visto pelo usuário ser uma URL melhor formatada.

- Os botões que organizam a lista de produtos por prateleira, ou por ordem crescente e decrescente de preço estão funcionando, utilizando filtros nas querys no banco de dados do Django.

- Foram adicionadas as visualizações relacionadas ao estoque, vendas e clientes. As visualizações foram de produtos mais vendidos, consumidores mais ativos, venda por dia da semana, vendas por seção e relação entre quantidade vendida e lucro bruto. Essas visualizações foram feitas com o `pandas` para a manipulação dos dados e utilizamos o `plotly` para exibir os gráficos dinâmicos no HTML.

## Bibliografia
Django. Fornecendo dados iniciais para modelos. **DjangoProject**. Disponível em: https://docs.djangoproject.com/pt-br/2.0/howto/initial-data/. Acesso em: 29 de novembro de 2021.
Stackoverflow. Writing pandas DataFrame to JSON in unicode. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/39612240/writing-pandas-dataframe-to-json-in-unicode. Acesso em: 29 de novembro de 2021.
Stackoverflow . How to write a Pandas Dataframe to Django model. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/34425607/how-to-write-a-pandas-dataframe-to-django-model. Acesso em: 30 de novembro de 2021.
Djang. The Django template language. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/templates/language/. Acesso em: 30 de novembro de 2021.
Django. Models. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/topics/db/models/. Acesso em: 30 de novembro de 2021.
KRUNAL. How To Convert Python List To JSON. **AppDividend**. Disponível em: https://appdividend.com/2019/11/13/how-to-convert-python-list-to-json-example/. Acesso em: 30 de novembro de 2021.
Django. Model instance reference. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/models/instances/. Acesso em: 30 de novembro de 2021.
Stackoverflow. How to remove all of the data in a table using Django. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/4532681/how-to-remove-all-of-the-data-in-a-table-using-django. Acesso em: 30 de novembro de 2021.
Stackoverflow. Convert Django Model object to dict with all of the fields intact. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact. Acesso em: 30 de novembro de 2021.
Stackoverflow. Append dictionary to data frame. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/51774826/append-dictionary-to-data-frame. Acesso em: 30 de novembro de 2021.
Django. The Django template language: for Python programmers. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/templates/api/. Acesso em: 30 de novembro de 2021.
Stackoverflow. Converting Django QuerySet to pandas DataFrame. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/11697887/converting-django-queryset-to-pandas-dataframe. Acesso em: 1 de dezembro de 2021.
Django. Django-admin and manage.py. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/django-admin/. Acesso em: 1 de dezembro de 2021.
Django. Making queries. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/topics/db/queries/. Acesso em: 1 de dezembro de 2021.
Plotly. Interactive HTML Export in Python. **Plotly**. Disponível em: https://plotly.com/python/interactive-html-export/. Acesso em: 1 de dezembro de 2021.
Plotly. Configuration in Python. **Plotly**. Disponível em: https://plotly.com/python/configuration-options/. Acesso em: 1 de dezembro de 2021.
Plotly. plotly.io.to_html. **Plotly**. Disponível em: https://plotly.com/python-api-reference/generated/plotly.io.to_html.html. Acesso em: 1 de dezembro de 2021.
RAMOS, Vinícius. O comando migrate do Django. **PythonAcademy**. Disponível em: https://pythonacademy.com.br/blog/o-comando-migrate-do-django. Acesso em: 1 de dezembro de 2021.
Django. QuerySet API reference. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/models/querysets/. Acesso em: 1 de dezembro de 2021.
YILDIRIN, Abdurrahin. Python Django Handling Custom Error Page. **Medium**. Disponível em: https://medium.com/@yildirimabdrhm/python-django-handling-custom-error-page-807087352bea. Acesso em: 1 de dezembro de 2021.
Django. Built-in template tags and filters. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/ref/templates/builtins/. Acesso em: 1 de dezembro de 2021.
Django. Writing views. **DjangoProject**. Disponível em: https://docs.djangoproject.com/en/3.2/topics/http/views/#customizing-error-views. Acesso em: 1 de dezembro de 2021.
Stackoverflow. Embedding a Plotly chart in a Django template. **Stackoverflow**. Disponível em: https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template/60933039#60933039. Acesso em: 1 de dezembro de 2021.