app = angular.module 'js.darg.app.shareholder', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'ShareholderController', ['$scope', '$http', 'Shareholder', ($scope, $http, Shareholder) ->

    $scope.shareholder = true
    $scope.countries = []
    $scope.languages = []
    $scope.errors = null

    $http.get('/services/rest/shareholders/' + shareholder_id).then (result) ->
        if result.data.user.userprofile.birthday != null
            result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday)
        $scope.shareholder = new Shareholder(result.data)
        if $scope.shareholder.user.userprofile.country
            $http.get($scope.shareholder.user.userprofile.country).then (result1) ->
                $scope.shareholder.user.userprofile.country = result1.data

    $http.get('/services/rest/country').then (result) ->
            $scope.countries = result.data.results

    $http.get('/services/rest/language').then (result) ->
            $scope.languages = result.data

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_shareholder = () ->
        if $scope.shareholder.user.userprofile.birthday
            # http://stackoverflow.com/questions/1486476/json-stringify-changes-time-of-date-because-of-utc
            date = $scope.shareholder.user.userprofile.birthday
            date.setHours(date.getHours() - date.getTimezoneOffset() / 60)
            $scope.shareholder.user.userprofile.birthday = date
        if $scope.shareholder.user.userprofile.country
            $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url
        if $scope.shareholder.user.userprofile.language
            $scope.shareholder.user.userprofile.language = $scope.shareholder.user.userprofile.language.iso
        $scope.shareholder.$update().then (result) ->
            if result.user.userprofile.birthday != null
                result.user.userprofile.birthday = new Date(result.user.userprofile.birthday)
            $scope.shareholder = new Shareholder(result)
            if $scope.shareholder.user.userprofile.country
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
            Raven.captureMessage('form error: ' + rejection.statusText, {
                level: 'warning',
                extra: { rejection: rejection },
            })

    # --- DATEPICKER
    $scope.datepicker = { opened: false }
    $scope.datepicker.format = 'd.MM.yy'
    $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker = ->
        $scope.datepicker.opened = true

]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
