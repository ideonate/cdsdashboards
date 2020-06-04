
it('login as dan', () => {
  cy.visit('/hub/home')

  cy.get('#username_input')
    .type('dan')

    cy.get('#password_input')
    .type('password')

  cy.get('form').submit()

  cy.get('#start')
    .should('contain', 'My Server')

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(4) > a')
    .should('contain', 'Dashboards')

})

