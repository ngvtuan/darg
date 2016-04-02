app = angular.module 'js.darg.app.start', ['js.darg.api', 'pascalprecht.translate']

app.config ['$translateProvider', ($translateProvider) ->
    $translateProvider.translations('de', django.catalog)
    $translateProvider.preferredLanguage('de')
]

app.controller 'StartController', ['$scope', '$http', 'CompanyAdd', 'Shareholder', 'User', 'Company', ($scope, $http, CompanyAdd, Shareholder, User, Company) ->

    # from server
    $scope.shareholders = []
    $scope.option_holders = []
    $scope.user = []
    $scope.total_shares = 0
    $scope.loading = true

    $scope.show_add_shareholder = false

    # empty form data
    $scope.newShareholder = new Shareholder()
    $scope.newCompany = new CompanyAdd()

    # FIXME - its not company specific
    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.shareholders.push item

    $http.get('/services/rest/user').then (result) ->
        $scope.user = result.data.results[0]
        # loop over ops and fetch corp data
        angular.forEach $scope.user.operator_set, (item, key) ->
            # get company data
            $http.get(item.company).then (result1) ->
                $scope.user.operator_set[key].company = result1.data
                # fetch operators for this company
                $http.get('/services/rest/company/'+result1.data.pk+'/option_holder').then (result2) ->
                    angular.forEach result2.data.results, (item) ->
                        $scope.option_holders.push item

    .finally ->
        $scope.loading = false

    $scope.$watchCollection 'shareholders', (shareholders)->
        $scope.total_shares = 0
        angular.forEach shareholders, (item) ->
            $scope.total_shares = item.share_count + $scope.total_shares

    $scope.add_company = ->
        if $scope.newCompany.founded_at
            $scope.newCompany.founded_at = $scope.newCompany.founded_at.toISOString().substring(0, 10)
        else
            delete $scope.newCompany.founded_at
        $scope.newCompany.$save().then (result) ->
            $http.get('/services/rest/user').then (result) ->
                $scope.user = result.data.results[0]
                # loop over ops and fetch corp data
                angular.forEach $scope.user.operator_set, (item, key) ->
                    $http.get(item.company).then (result1) ->
                        $scope.user.operator_set[key].company = result1.data
                        # fetch operators for this company
                        $http.get('/services/rest/company/'+result1.data.pk+'/option_holder').then (result2) ->
                            angular.forEach result2.data.results, (item) ->
                                $scope.option_holders.push item

            $http.get('/services/rest/shareholders').then (result) ->
                angular.forEach result.data.results, (item) ->
                    $scope.shareholders.push item
        .then ->
            # Reset our editor to a new blank post
            $scope.company = new Company()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.add_shareholder = ->
        $scope.newShareholder.$save().then (result) ->
            $scope.shareholders.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newShareholder = new Shareholder()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.show_add_shareholder_form = ->
        $scope.show_add_shareholder = true

    $scope.hide_form = ->
        $scope.show_add_shareholder = false

    $scope.goto_shareholder = (shareholder_id) ->
        window.location = "/shareholder/"+shareholder_id+"/"
]
