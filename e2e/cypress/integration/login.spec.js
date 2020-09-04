
it('login as dan', () => {

  do_login()

  cy.get('#start')
    .should('contain', 'My Server')

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(5) > a')
    .should('contain', 'Dashboards').click()

  cy.get('#start')
    .should('contain', 'New Dashboard')

})

