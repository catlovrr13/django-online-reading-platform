// components
// import GridMotion from "@/components/GridMotion";
import { Button } from "@/components/ui/button";
import ScrollFloat from "@/components/ScrollFloat";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { Card, CardContent } from "@/components/ui/card";

// media

// function
import { useTheme } from "@/components/theme-provider";

export const iframeHeight = "800px";

export default function Page() {
  const { theme } = useTheme();
  const heroBG =
    theme === "dark" ? `bg-stone-900 opacity-40` : `bg-stone-200 opacity-40`;
  const cardAd =
    theme === "dark" ? `bg-stone-100 opacity-10` : `bg-stone-900 opacity-20`;

  return (
    <>
      <div className="flex flex-col gap-0 justify-center">
        {/* hero section */}
        <div
          className={`
          // delete this \/ after finishing 
          min-h-screen 
          ${heroBG} p-10 flex flex-col md:flex-row`}
        >
          <div className="">welcome</div>
          <div className="">pic here</div>
        </div>

        {/* genre */}
        <div
          className={`overflow-hidden w-full max-w-2xl flex flex-col gap-5 p-5 justify-center items-center`}
        >
          <ScrollFloat
            animationDuration={3}
            ease="back.inOut(2)"
            scrollStart="center bottom+=50%"
            scrollEnd="bottom bottom-=40%"
            stagger={0.04}
          >
            Genres
          </ScrollFloat>
          <Carousel
            opts={{
              align: "start",
            }}
            className="w-full max-w-[12rem] sm:max-w-xs md:max-w-sm"
          >
            <CarouselContent>
              {Array.from({ length: 5 }).map((_, index) => (
                <CarouselItem key={index} className="basis-1/2 lg:basis-1/3">
                  <div className="p-1">
                    <Card>
                      <CardContent className="flex aspect-square items-center justify-center p-6">
                        <span className="text-3xl font-semibold">
                          {index + 1}
                        </span>
                      </CardContent>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>

        {/* subscription ad */}
        <div className={`h-100 ${heroBG} flex flex-col p-10 justify-center`}>
          <div className={`h-50 w-full max-w-3xl mx-auto ${cardAd}`}></div>
        </div>
      </div>
    </>
  );
}
