# ReCollect

ReCollect is supported by the generic [ICS](/doc/source/ics.md) source. For all available configuration options, please refer to the source description.


## How to get the configuration arguments

- To get the URL, search your address in the recollect form of your home town.
- Click "Get a calendar", then "Add to Google Calendar".
- The URL shown is your ICS calendar link, for example.
  ```plain
  https://recollect.a.ssl.fastly.net/api/places/BCCDF30E-578B-11E4-AD38-5839C200407A/services/208/events.en.ics?client_id=6FBD18FE-167B-11EC-992A-C843A7F05606
  ```
- You can strip the client ID URL parameter to get the final URL: `https://recollect.a.ssl.fastly.net/api/places/BCCDF30E-578B-11E4-AD38-5839C200407A/services/208/events.en.ics`

known to work with:
|Region|Country|URL|
|-|-|-|
|Ottawa, ON|Canada|[ottawa.ca](https://ottawa.ca/en/garbage-and-recycling/recycling/garbage-and-recycling-collection-calendar)|
|Simcoe County, ON|Canada|[simcoe.ca](https://www.simcoe.ca/dpt/swm/when)|
|City of Bloomington, IN|USA|[api.recollect.net/r/area/bloomingtonin](https://api.recollect.net/r/area/bloomingtonin)|
|City of Cambridge, MA|USA|[cambridgema.gov](https://www.cambridgema.gov/services/curbsidecollections)|

and probably a lot more.

## Examples

### Cambridge, MA, USA

```yaml
waste_collection_schedule:
  sources:
    - name: ics
      args:
        split_at: '\, (?:and )?|(?: and )'
        url: https://recollect.a.ssl.fastly.net/api/places/F2BCBBF2-ACC9-11E8-B4BD-CFDD30C1D4D8/services/761/events.en-US.ics
```
### Ottawa, ON, Canada

```yaml
waste_collection_schedule:
  sources:
    - name: ics
      args:
        split_at: '\, (?:and )?|(?: and )'
        url: https://recollect.a.ssl.fastly.net/api/places/BCCDF30E-578B-11E4-AD38-5839C200407A/services/208/events.en.ics
```