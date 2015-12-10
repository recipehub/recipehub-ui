(function(){

    var prefix = '/api/v1/search/';

    angular.module('recipehub')
        .service('SearchService', ['$http', function searchService($http) {
            this.search = function (q) {
                return $http.get(prefix, {
                    params: {
                        q: q
                    }
                });
            };
        }]);
})();
