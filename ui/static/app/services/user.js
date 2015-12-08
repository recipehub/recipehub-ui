(function(){

    var prefix = '/api/v1/comment/';

    angular.module('recipehub')
        .service('UserService', ['$http', function recipeService($http) {
            this.getCurrentUser = function () {
                return $http.get(prefix);
            };

        }]);
})();
