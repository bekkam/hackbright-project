describe("Route Name Test Suite", function () {

    it("should return false if argument is less than two", function () {
        var length = checkMinimumInputLength(1);
        expect(length).toBe(false);
    });

    it("should return true if argument is greater than or equal to two", function () {
        expect(checkMinimumInputLength(2)).toBeTruthy();
    });

});


describe("Date Format Test Suite", function () {
// month
    it("should return false if month argument is not two numbers", function () {
        expect(checkDateFormat("001/12/2016")).toBeFalsy();
        expect(checkDateFormat("1/12/2016")).toBeFalsy();
    });
// day
    it("should return false if day argument is not two numbers", function () {
        expect(checkDateFormat("01/120/2016")).toBeFalsy();
        expect(checkDateFormat("01/1/2016")).toBeFalsy();
    });

// year
    it("should return false if year argument is not four numbers", function () {
        expect(checkDateFormat("01/12/20166")).toBeFalsy();
        expect(checkDateFormat("01/12/201")).toBeFalsy();
    });
});


describe("Date Boundaries Test Suite", function () {
// month
    it("should return false if month argument is not between 1 and 12", function () {
        expect(checkDateBoundaries("20/10/2016")).toBeFalsy();
        expect(checkDateBoundaries("00/10/2016")).toBeFalsy();
    });
// day
    it("should return false if day argument is not between 1 and 31", function () {
        expect(checkDateBoundaries("00/10/2016")).toBeFalsy();
        expect(checkDateBoundaries("32/10/2016")).toBeFalsy();
    });

    it("should return false if day argument is out of range for the specified month", function () {
        expect(checkDateBoundaries("04/31/2016")).toBeFalsy();
    });
// future date
    it("should return false if date given is in the future", function () {
        expect(checkDateBoundaries("10/31/2017")).toBeFalsy();
    });
});


describe("Duration Test Suite", function () {

    it("should return false if argument does not consist of all and only digits", function () {
        expect(checkDurationType("we")).toBeFalsy();
        expect(checkDurationType("33g")).toBeFalsy();
        expect(checkDurationType("33!")).toBeFalsy();
        expect(checkDurationType("33 ")).toBeFalsy();
        expect(checkDurationType("3.3")).toBeFalsy();
    });
});
