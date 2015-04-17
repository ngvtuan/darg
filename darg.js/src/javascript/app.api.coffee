app = angular.module 'js.darg.api', ['ngResource']

app.factory 'Shareholder', ['$resource', ($resource) ->
    $resource '/services/rest/shareholders/:id', id: '@id'
]

app.factory 'Company', ['$resource', ($resource) ->
    $resource '/services/rest/company/:id', id: '@id'
]

app.factory 'User', ['$resource', ($resource) ->
    $resource '/services/rest/user/:id', id: '@id'
]
