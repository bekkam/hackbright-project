describe("Run Test Suite", function () {

    it("should return false if argument is less than two", function () {
        var length = checkMinimumInputLength(1);
        expect(length).toBe(false);
    });

    it("should return true if argument is greater than or equal to two", function () {
        expect(checkMinimumInputLength(2)).toBeTruthy();
    });

});
