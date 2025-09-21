## 💡 Projeto sugerido: **Sistema de Blog com Autores, Postagens e Comentários**

### Regras principais

1. **Usuários (autores)** podem se cadastrar e fazer login (**Flask-Login**).
2. Cada **usuário** pode criar vários **posts** (relação **1\:N**).
3. Cada **post** pode receber vários **comentários**.
4. Cada **comentário** pertence a um usuário (quem comentou) e a um post (**N:1** duplo).
5. O sistema deve diferenciar:

   * Usuário logado pode **criar posts** e **comentar**.
   * Só o autor do post pode **editar/excluir** seu próprio post.
   * Só o autor do comentário pode **excluir** seu comentário.


---

### Funcionalidades mínimas para treinar

1. **Cadastro/Login/Logout** com `Flask-Login`.
2. **Página inicial** listando posts de todos os usuários.
3. **Página de perfil** mostrando posts e comentários do usuário.
4. **CRUD de posts** (apenas o dono pode editar/excluir).
5. **Sistema de comentários** nos posts (apenas logado pode comentar, dono do comentário pode excluir).

---

### Extras para praticar ainda mais

* Adicionar **hash de senha** com `werkzeug.security`.
* Criar **roles** (ex: admin que pode apagar qualquer post/comentário).
* Implementar **paginação** nos posts.
* Criar **like/dislike** em posts e comentários (tabela associativa extra).

---

👉 Esse projeto vai te forçar a juntar:

* **Autenticação com Flask-Login**
* **Relacionamentos 1\:N e N:1**
* **Controle de permissões**
* **Boas práticas de segurança (hash de senha)**

---

