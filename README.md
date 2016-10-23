# Gift the Code Hackathon - Second Harvest
This repo is our submission for [Capital One's Gift the Code Hackathon](http://giftthecode.ca/)!

<p align="center">
  <img src=images/giftthecode.jpg alt="Sublime's custom image" style="width: 600px;" style="height: 200px;"/>
</p>

The details of the hackathon, the charity we worked for and our solution are provided below. Enjoy!

- [The Charity](#the_charity)
- [The Challenge](#the_challenge)
- [Solution Overview](#solution_overview)
- [Deep Dive](#deep_dive)
  - [Website](#website)
  - [Analytics](#analytics)
  - [Tech Stack](#tech_stack)
- [Next Steps](#next_steps)
- [The Team](#the_team)
  - [Questions](#questions)

## <a name="the_charity"></a>The Charity

<p align="center">
  <img src=images/second_harvest_logo.jpg alt="Sublime's custom image"/>
</p>

<br/>

[Second Harvest](http://www.secondharvest.ca/) (SH) is a food rescue program based out of Toronto, Ontario that picks up donated or surplus food, which would otherwise go to waste, and deliver that food to community agencies across Toronto and the Greater Toronto Area.

<br/>

## <a name="the_challenge"></a>The Challenge

The challenge posed by SH tasked us with creating a solution that allows SH to leverage the potential benefits of its data.

Every year, SH picks up and delivers $15M of food to different partner organisations. The team is always busy minimising the time spent transiting the food and maximising the freshness of them when delivered to 200k people's plates. However, the data reporting and analytics currently experience a substantial lag, given the work associated with such tasks.

In our first empathy interview with the SH team, Jennifer and Shane, we gathered 3 main problems they're facing.

* Data intake and processing: There are 2 main data tables essential to SH's food operations: record of each delivery (location, routes, quantity and type of food) and record of each donor's survey response (number and demographic of people served, how has SH helped and how could it better help). Traditionally SH's delivery drivers, agencies and volunteers record all the data manually, and a survey is sent out every year. Currently SH is piloting a new app which simplifies the recording and the transmission of some of the data.
  + We need to facilitate the intake of this data,  process it and derive usable insights as soon as it comes in.


* Status report: SH currently uses Excel to aggregate the data to produce reports. The team is currently tracking a few metrics such as %perishable food, an important ratio due to the rarity of fresh produce in the general donation environment and SH's expertise with quick deliveries. Given all the work SH does, it would also like to generate more intuitive figures to present to the government for additional assistance and partnership.
  + In addition increase frequency of data intake, we aim to automate the processing of more frequently collected data and increase the flexibility in manipulating the data to explore more views.


* Reports are now retrospective on the past fiscal year. SH would like use it to forecast key metrics of its future operations and better allocate its capacities.

## <a name="solution_overview"></a>Solution Overview

Our [solution](http://ec2-52-87-205-105.compute-1.amazonaws.com:12345/) to SH's needs is an integrated and semi-automated system which collects, processes and generates useful insights, while allowing for customisation and data exploration.

<p align="center">
<img src=images/datamanagementflow-02.jpg alt="Solution Overview" style="width: 600px;" style="height: 600px;" />

</p>

* The intake process now involves a simple drag and drop of data generated by third party apps such as the delivery drivers. The simplification is crucial in ensuring that the most up-to-date data is always saved and available for further analyses. We also facilitate the combination of survey and delivery data into one table in order to later generate more comprehensive views (e.g. which demographic groups are consuming which types of food).
<br/>

* With the data, we have created two sets of reports: an interactive map with key metrics such as quantity and value of food delivered or %perishable food, and a series of charts which helps.

  + The map generates a more intuitive visualisation of the data, allowing the SH team pinpoint insights by neighbourhood and routes, around which the SH operations are organised. This automated process drives more effortless and frequent reports which monitors specific groups' needs and helps identifying issues more quickly. The added interactivity and data manipulation capabilities replaces some of the manual work in Excel which hinders data exploration. They allow the SH team to try creating more views which could uncover more insights. For instance, we've found certain routes and donors which often do not have any food available when the delivery driver arrives.


* Given SH's limited experience with forecasting, we've created views of historical data by day of the week and hour of the day, which shows that many deliveries happen on Friday morning. In addition to the interactivity with location, time, demographics and type of food, this should allow the SH team to predict their future needs and capacities.



<br/>

## <a name="deep_dive"></a>A Deep Dive...

As we prepare for a deep dive into the intricacies of our app, our first order of business is.....
<br/>
...
<br/>
....
<br/>
.....
<br/>
......
<br/>
.......
<br/>
.........
<br/>
...........
<br/>
..............
<br/>
..................
<br/>
.......................


<p align="center">
  <img src=images/suitup.jpg alt="Suit up" style="width: 800px;" style="height: 800px;" />

</p>

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

Now that you are *properly equipped*, let's **PLUNGE** in....to the [website](http://ec2-52-87-205-105.compute-1.amazonaws.com:12345/)
<br/>
<br/>
<br/>
<br/>

### <a name="website"></a>Website

The landing page of the website features a interactive data vizualization for all of SH's delivery and pickup data. The bubbles are colour coded according to whether they represent a pickup or a delivery. A slider is present at the top, allowing the user to switch between different yearly views of the data.

<br/>
<br/>
<br/>

<p align="center">
  <img src=images/screen1.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>

<br/>
<br/>
<br/>

When the user hovers over a bubble, an informative tooltip pops up, showing relevant information about the specific location. Facts such as the total food delivered, the average nutrient ratio and the average perishable ratio for the selected year are provided.

<br/>
<br/>
<br/>

<p align="center">
  <img src=images/screen6.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>

<br/>
<br/>
<br/>

Next, the user is guided to a secure login page so that the SH team can access their internal data and reports. The reports are discussed further in the [analytics section](#analytics).

<br/>
<br/>
<br/>

<p align="center">
  <img src=images/screen2.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>

<br/>
<br/>
<br/>

Users can then upload their deliver/pickup and survey data using the file uploading system shown below.

<br/>
<br/>
<br/>

<p align="center">
  <img src=images/screen3.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>

<br/>
<br/>
<br/>

<p align="center">
  <img src=images/screen4.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>

<br/>
<br/>
<br/>

### <a name="analytics"></a>Analytics
A snapshot of the base analytics package is shown below.

<br/>
<br/>
<br/>
<p align="center">
  <img src=images/screen5.png alt="Sublime's custom image" style="width: 800px;" style="height: 800px;"/>
</p>
<br/>
<br/>
<br/>

### <a name="tech_stack"></a>Tech Stack
An overview of the various technologies we used is provided below.
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

<p align="center">
  <img src=images/techdiagram.jpg alt="Tech Stack" style="width: 600px;" style="height: 600px;" />

</p>

<br/>
<br/>
<br/>

## <a name="next_steps"></a>Next Steps

Our entire application and all associated technology requirements is deployed on a single EC2 server.

To maximize the ease of utilization for Second Harvest, we have created a snapshot of our EC2 instance so that they can easily replicate the application with a few clicks.

More info can be found @ http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/launch-more-like-this.html

[The team](#the_team) can be consulted for any deployment questions.

<br/>
<br/>
<br/>
## <a name="the_team"></a>The Team

* **Darren Lin** - *Data Scientist @ Capital One*
* **Oliver Zhang** - *Business Analyst @ Capital One*
* **Flora Zhang** - *Data Engineer @ Capital One*
* **Kevin Seto** - *Graphic Design Student @ OCAD*
* **Lucy Chen** - *Interaction Designer @ Veeva*
* **Ian Whitestone** - *Data Scientist @ Capital One*
<br/>
<br/>
<br/>

### <a name="questions"></a>Questions?

Feel free to email: ianjameswhitestone@gmail.com or darrenlin17@gmail.com for questions.
<br/>
<br/>
<br/>
<p align="center">
  <img src=images/mango.jpeg alt="Sublime's custom image"/>
</p>
<br/>
<br/>
<br/>
