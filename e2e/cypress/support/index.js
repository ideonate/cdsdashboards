
Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from
  // failing the test
  return false
})

do_login = () => {
  
  cy.visit('/hub/home')

  cy.get('#username_input')
    .type('dan')

    cy.get('#password_input')
    .type('password')

  cy.get('form').submit()

}

do_create_and_start_dashboard = (name, path, framework) => {

  cy.visit('/hub/home')

  cy.get('#thenavbar > ul:nth-child(1) > li:nth-child(5) > a')
    .should('contain', 'Dashboards').click()

  cy.get('#start')
    .should('contain', 'New Dashboard').click()

  cy.get('#dashboard-name')
    .type(name)

  cy.get('#dashboard-start-path')
    .type(path)

  cy.get('#presentation_type')
    .select(framework)

  cy.get('#main > div > div > form > div > input[type=submit]')
    .click()

}

do_stop_dashserver = (id) => {
  cy.visit('/hub/home')

  cy.wait(500) // There is probably a better way of course!

  cy.get('#stop-'+id)
    .should('be.visible')
    .should('contain', 'stop').click()

  cy.get('#start-'+id)
    .should('be.visible', { timeout: 20000 })
    .should('contain', 'start') // Appears when stop complete

}
