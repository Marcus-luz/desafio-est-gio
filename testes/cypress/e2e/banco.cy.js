describe('Jornada do Usuário - E2E Frontend', () => {
  
  beforeEach(() => {
    cy.visit('http://localhost:5173')
  })

  it('Deve fazer login e renderizar o dashboard', () => {
    cy.get('input[placeholder="Digite seu nome"]').type('Avaliador')
    cy.get('button').contains('ACESSAR').click()
    
    cy.contains('Olá, Avaliador').should('be.visible')
    
    // CORREÇÃO: Trocamos 'Saldos Disponíveis' (que não existe mais) 
    // por 'Fazer Saque' (que é um título real da nossa tela)
    cy.contains('Fazer Saque').should('be.visible')
    cy.contains('Histórico de Atividades').should('be.visible')
  })

  it('Deve bloquear transferência para a mesma conta (Edge Case)', () => {
    cy.get('input[placeholder="Digite seu nome"]').type('Avaliador')
    cy.get('button').contains('ACESSAR').click()

    cy.get('select').eq(1).select('1001')
    cy.get('select').eq(2).select('1001')
    cy.get('input[placeholder="Valor (R$)"]').eq(1).type('50')
    
    cy.get('button').contains('Transferir Agora').click()

    cy.contains('A conta de origem e destino não podem ser iguais.').should('be.visible')
  })
})