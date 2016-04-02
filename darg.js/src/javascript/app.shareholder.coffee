app = angular.module 'js.darg.app.shareholder', ['js.darg.api', 'xeditable', 'pascalprecht.translate']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
]

app.controller 'ShareholderController', ['$scope', '$http', 'Shareholder', ($scope, $http, Shareholder) ->

    $scope.shareholder = true
    $scope.errors = null

    $http.get('/services/rest/shareholders/' + shareholder_id).then (result) ->
        result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday)
        $scope.shareholder = new Shareholder(result.data)
        $http.get($scope.shareholder.user.userprofile.country).then (result1) ->
            $scope.shareholder.user.userprofile.country = result1.data

    $http.get('/services/rest/country').then (result) ->
            $scope.countries = result.data.results

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_shareholder = () ->
        if $scope.shareholder.user.userprofile.country
            $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url
        if $scope.shareholder.user.userprofile.birthday
            $scope.shareholder.user.userprofile.birthday = $scope.shareholder.user.userprofile.birthday.toISOString().substring(0, 10)
        $scope.shareholder.$update().then (result) ->
            result.user.userprofile.birthday = new Date(result.user.userprofile.birthday)
            $scope.shareholder = new Shareholder(result)
            $http.get($scope.shareholder.user.userprofile.country).then (result1) ->
                $scope.shareholder.user.userprofile.country = result1.data
        .then ->
            # Reset our editor to a new blank post
            #$scope.company = new Company()
            undefined
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
