# ZAIO deployment on GCP

This is a guide to run a fully functional [Zentral](https://github.com/zentralopensource/zentral) instance on **Google Cloud Platform**. 
We will be using the **Zentral all in one** pre-build image.

*Note: We also provide a guide for an AWS based setup - please look [here](../zaio-aws).*

To follow this tutorial, you will need an admin access to the Google Cloud Platform console ([Getting started](https://cloud.google.com/gcp/getting-started/))

*Note: This tutorial is only a first step toward a production deployment on Google Cloud.*

## Google Cloud Platform setup

You will need to pick a **project**, and think about a **region** where you want to store the image, and start the instance. For the rest of this tutorial, it will be `My First Project` and `europe-west-3`.

## Import the image in your project

Open the [Create an image](https://console.cloud.google.com/compute/imagesAdd) form.

In the **Name** field, specify a unique name for the image. We will use `zentral-all-in-one`.

Click the **Source** menu and select _Cloud Storage file_.

Enter the path to the public _Zentral all in one_ image file:

```
zentralopensource/zentral_all_in_one.json
```

Pick a location.

![Create image form example](../../images/deployment/zaio-gcp/create_zaio_image.png)

Click on the **Create** button to import the image. The process can take several minutes. The image is now included on the [Images page](https://console.cloud.google.com/compute/images).

## Setup the firewall rules

*Note: We will be working with the default VPC. This is not recommended for production.*

At the minimum, for this tutorial, we will need access to the 22, 80, and 443 ports. If you want to test the filebeat / logstash log shipping, you will also need access to the 5044 port.
 
The default rules on the default network should be enough. You will need to add a rule to open the 5044 port. You can skip this section if you do not intend to test filebeat / logstash.

Review the [existing firewall rules](https://console.cloud.google.com/networking/firewalls/list), and [add a new firewall rule](https://console.cloud.google.com/networking/firewalls/add) if necessary.

In the **Name** field, specify a unique name for your rule. We will use `default-allow-logstash`.

Make sure that you attach the rule to the correct network (`default` per default).

Click the **Targets** menu and select _Specified target tags_

In the **Target tags** field, specify a unique name for your tag. We will use `logstash`. We will use this network tag on the instance later, to attach this firewall rule to it.

Click the **Source filter** menu and select _IP ranges_

In the **Source IP ranges** specify `0.0.0.0/0` as the range of IP addresses allowed.

*Note: this rule open the 5044 to the world. You can be more restrictive if you like*

In the **Protocols and ports** menu, select *Specified protocols and ports*, tick the _tcp_ bock, and specify _5044_ as the port number.

Click on the **Create** button to create the firewall rule.

## Create the instance

Open the [Create an instance](https://console.cloud.google.com/compute/instancesAdd) form.

In the **Name** field, specify a unique name for your instance. We will use `zentral-all-in-one`.

Select a **Region** and a **Zone**.

The default _General-purpose_ **Machine family**, and _n1-standard-1_ **Machine type** are OK to test Zentral.

![Create instance form first sections](../../images/deployment/zaio-gcp/create_instance_top_form.png)

In the **Boot disk** section, click on the [Change] button, go to the [Custom images] tab. Select the `zentral-all-in-one` image that you created at the beginning of this tutorial.

![Select zentral-all-in-one custom image](../../images/deployment/zaio-gcp/select_image.png)

You can start with one 10GB SSD persistent disk. But that would be only enough to store a limited amount of events. As a rule of thumb, you will need about 7GB + 1GB for every million of events stored, but that can vary a lot depending on your inventory sources, and the kind of events you are collecting.

![SSD persistent disk size](../../images/deployment/zaio-gcp/ssd_persistent_disk.png)

This is what you should see in the *Boot disk* menu:

![zentral-all-in-one-image-selected](../../images/deployment/zaio-gcp/boot_disk_selected.png)

We will use the **Compute engine default service account** and the **default access scopes**. Again, not recemmended for production.

In the **Firewall** section, tick the _Allow HTTP traffic_ and _Allow HTTPS traffic_ boxes.

If you want to try the filebeat / logstash functionality, you need to add the `logstash` network tag you have created to the instance, in order to attach the firewall rule. You can skip this step if you do not want to try this integration. Expand the _Management, security, disks, networking, sole tenancy_ section, open the _Networking_ tab, and add _logstash_ in the **Network tags** field. 

![Create instance form network section](../../images/deployment/zaio-gcp/network_section.png)

Click on the **Create** button to launch the instance.

## Setup the domain name(s) for your instance

Zentral requires at leat one domain name resolving to the IP address of the launched instance. If you want to ship logs with filebeat, and experiment with the MDM, you will need a second domain name (to separate the endpoints requiring client certificate authentication).

1. In the Google Cloud console, [find the public IP address of the instance](https://console.cloud.google.com/compute/instances) that is starting. No need to wait for the instance to be fully up.
2. Use this IP to setup a first required A record. (_zentral.example.com_ for the rest of this tutorial)
3. You can setup a second A record pointing to be able to test all the Zentral functionalities. (_zentral-clicertauth.example.com_ for the rest of this tutorial)
4. Test the resolution of these records! You cannot move on to the next section before they are setup.

## Log onto your instance

You can open a ssh session via the Google Cloud. Click on the instance in the [list of all instance](https://console.cloud.google.com/compute/instances). At the top of the instance page, open the **Remote access / SSH** menu and select _Open in browser window_. A new tab will open and a ssh session will start.

![open ssh in browser window](../../images/deployment/zaio-gcp/open_ssh_in_browser_window.png)

Once logged in, you can use a [command line tool to setup your instance](../zaio-setup). Because this last step is the same for a AWS deployment, we have kept it on a separate wiki page.
