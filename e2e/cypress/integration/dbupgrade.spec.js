
it('login as dan', () => {
  
  do_login()

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(4) > a')
    .should('contain', 'Dashboards').click()

  cy.get('.dashboard-edit-form input')
    .should('have.value', 'Upgrade Database').click()

  cy.get('#main')
    .should('contain', 'Database upgrade successful!')

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(4) > a')
    .should('contain', 'Dashboards').click()

  cy.get('#start')
    .should('contain', 'New Dashboard')

})

