# Sefton Council

Support for schedules provided by [Sefton Council](https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/), serving the
district of Sefton, UK.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
    sources:
    - name: sefton_gov_uk
      args:
        Postcode: Postcode
        Streetname: Streetname
        House Number Or Name: houseNumberOrName
```

### Configuration Variables

**Postcode**  
*(string) (required)*

**Streetname**
*(string) (required)*

**House Name or Number**
*(string) (required)*

## Example

```yaml
waste_collection_schedule:
    sources:
    - name: sefton_gov_uk
      args:
        Postcode: "L20 6GF"
        Streetname: "Ken Mews"
        houseNumberOrName: "1"
```

## How to find the values for arguments above

Go to the Sefton "When is my Bin Collection Day?" page - the postcode and streetname arguments are the same values you'd enter on the first page of the form. The House Number or Name value is the string/number that appears before the streetname in the dropdown on the second page - e.g. if the dropdown shows "1A Liverpool Road" you should enter "1A" as your House Number or Name value.
