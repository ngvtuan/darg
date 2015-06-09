app = angular.module 'js.darg.api', ['ngResource']

app.factory 'Shareholder', ['$resource', ($resource) ->
    $resource '/services/rest/shareholders/:id', id: '@id'
]

app.factory 'CompanyAdd', ['$resource', ($resource) ->
    $resource '/services/rest/company/add/'
]

app.factory 'User', ['$resource', ($resource) ->
    $resource '/services/rest/user/:id', id: '@id'
]

app.factory 'Position', ['$resource', ($resource) ->
    $resource '/services/rest/position/:id', id: '@id'
]

app.factory 'Invitee', ['$resource', ($resource) ->
    $resource '/services/rest/invitee/:id', id: '@id'
]
