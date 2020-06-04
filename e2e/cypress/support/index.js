
do_login = () => {
  
  cy.visit('/hub/home')

  cy.get('#username_input')
    .type('dan')

    cy.get('#password_input')
    .type('password')

  cy.get('form').submit()

}

