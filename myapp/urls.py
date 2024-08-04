from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.mysite, name='mysite'),
    path('adicionar_equipamento/', views.adicionar_equipamento, name='adicionar_equipamento'),
    path('equipamento_sucesso/', views.equipamento_sucesso, name='equipamento_sucesso'),
    path('lista_equipamentos/', views.listar_equipamentos, name='lista_equipamentos'),
    path('editar_equipamento/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('apagar_equipamento/<int:id>/', views.apagar_equipamento, name='apagar_equipamento'),
    path('equipamento/<int:id>/', views.detalhes_equipamento, name='detalhes_equipamento'),
    path('api/equipamento/<int:equipamento_id>/preco_diaria/', views.get_preco_diaria, name='get_preco_diaria'),
    path('api/equipamento/<int:equipamento_id>/disponibilidade/', views.get_disponibilidade, name='get_disponibilidade'),
    path('api/equipamento/<int:equipamento_id>/valor_diaria/', views.get_valor_diaria, name='get_valor_diaria'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('cliente/', views.cliente, name='cliente'),
    path('clientes/verificar/', views.verificar_cliente, name='verificar_cliente'),
    path('api/verificar_cpf/', views.verificar_cpf, name='verificar_cpf'),
    path('cancelar_agendamento/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('painel/', views.painel, name='painel'),
    path('adicionar_categoria/', views.adicionar_categoria, name='adicionar_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('apagar_categoria/<int:id>/', views.apagar_categoria, name='apagar_categoria'),
    path('gerenciar_faqs/', views.gerenciar_faqs, name='gerenciar_faqs'),
    path('faq/', views.listar_faqs, name='listar_faqs'),
    
]