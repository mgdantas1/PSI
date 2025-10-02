## 📝 Atividade – Sistema de Professores, Disciplinas e Alunos

### Regras:

1. Um **Professor** pode ministrar várias **Disciplinas**. (relação **1\:N**)
2. Uma **Disciplina** pode ter vários **Alunos**, e um **Aluno** pode cursar várias **Disciplinas**. (relação **N\:N**)
3. Cada **Aluno** deve poder ser matriculado em uma ou mais **Disciplinas**.
4. Você deve conseguir:

   * Cadastrar **professores**.
   * Cadastrar **disciplinas** vinculando a um professor.
   * Cadastrar **alunos**.
   * Matricular um aluno em uma disciplina.
   * Listar todas as disciplinas que um aluno está cursando.
   * Listar todos os alunos de uma disciplina.

---

### 🔨 Tarefas para você implementar

1. Criar rotas para:

   * `/novo_professor`
   * `/nova_disciplina`
   * `/novo_aluno`
   * `/matricular_aluno` (escolher aluno + disciplina)
2. Criar página inicial `/` que mostre:

   * Todos os alunos e as disciplinas em que estão matriculados.
   * Ou, se preferir, todos os professores e suas disciplinas.

---
