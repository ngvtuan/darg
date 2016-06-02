app = angular.module 'js.darg.app.positions', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
    $translateProvider.useSanitizeValueStrategy('escaped')
]

app.controller 'PositionsController', ['$scope', '$http', 'Position', 'Split', ($scope, $http, Position, Split) ->
    $scope.positions = []
    $scope.shareholders = []
    $scope.securities = []

    $scope.show_add_position = false
    $scope.show_add_capital = false
    $scope.show_split_data = false
    $scope.show_split = false
    $scope.newPosition = new Position()
    $scope.newSplit = new Split()

    $http.get('/services/rest/position').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.positions.push item

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            if item.user.userprofile.birthday
                item.user.userprofile.birthday = new Date(item.user.userprofile.birthday)
            $scope.shareholders.push item

    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    $scope.add_position = ->

        $scope.newPosition.$save().then (result) ->
            $scope.positions.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.show_add_position = false
            $scope.show_add_capital = false
            $scope.newPosition = new Position()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error', {
                level: 'warning',
                extra: { rejection: rejection },
            })

    $scope.delete_position = (position) ->
        $http.delete('/services/rest/position/'+position.pk).then (result) ->
            $scope.positions = []
            $http.get('/services/rest/position').then (result1) ->
                angular.forEach result1.data.results, (item) ->
                    $scope.positions.push item

    $scope.confirm_position = (position) ->
        $http.post('/services/rest/position/'+position.pk+'/confirm').then (result) ->
            $scope.positions = []
            $http.get('/services/rest/position').then (result1) ->
                angular.forEach result1.data.results, (item) ->
                    $scope.positions.push item

    $scope.add_split = ->
        $scope.newSplit.$save().then (result) ->
            $scope.positions = result.data
        .then ->
            $scope.newSplit = new Split()
        .then ->
            $scope.errors = null
            $scope.show_split = false
        , (rejection) ->
            $scope.errors = rejection.data
            Raven.captureMessage('form error', {
                level: 'warning',
                extra: { rejection: rejection },
            })

    $scope.show_add_position_form = ->
        $scope.show_add_position = true
        $scope.show_add_capital = false
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.toggle_show_split_data = ->
        if $scope.show_split_data
            $scope.show_split_data = false
        else
            $scope.show_split_data = true

    $scope.show_add_capital_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = true
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.hide_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = false
        $scope.newPosition = new Position()
        $scope.show_split = false

    $scope.show_split_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = false
        $scope.newSplit = new Split()
        $scope.show_split = true

    # --- DATEPICKER
    $scope.datepicker = { opened: false }
    $scope.datepicker.format = 'd. MMM yyyy'
    $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false,
    }
    $scope.open_datepicker = ->
        $scope.datepicker.opened = true


]
