export const calculations = (data) => {
  let totalRevenue = 0;
  let missedRevenue = 0;

  let numberOfCarsWithTypes = [
    { type: "compact", servedCount: 0, missedCount: 0 },
    { type: "medium", servedCount: 0, missedCount: 0 },
    { type: "full-size", servedCount: 0, missedCount: 0 },
    { type: "class 1 truck", servedCount: 0, missedCount: 0 },
    { type: "class 2 truck", servedCount: 0, missedCount: 0 },
  ];
  for (let item of data) {
    if (item.is_added === true) {
      totalRevenue += item.revenue;
      switch (item.type) {
        case "compact":
          numberOfCarsWithTypes[0].servedCount += 1;
        case "medium":
          numberOfCarsWithTypes[1].servedCount += 1;
        case "full-size":
          numberOfCarsWithTypes[2].servedCount += 1;
        case "class 1 truck":
          numberOfCarsWithTypes[3].servedCount += 1;
        case "class 2 truck":
          numberOfCarsWithTypes[4].servedCount += 1;
      }
    } else {
      missedRevenue += item.revenue;
      switch (item.type) {
        case "compact":
          numberOfCarsWithTypes[0].missedCount += 1;
        case "medium":
          numberOfCarsWithTypes[1].missedCount += 1;
        case "full-size":
          numberOfCarsWithTypes[2].missedCount += 1;
        case "class 1 truck":
          numberOfCarsWithTypes[3].missedCount += 1;
        case "class 2 truck":
          numberOfCarsWithTypes[4].missedCount += 1;
      }
    }
  }
  let final_arr = [totalRevenue, missedRevenue, numberOfCarsWithTypes];
  return final_arr;
};
